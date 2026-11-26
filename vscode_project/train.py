"""学習スクリプト。

使い方:
    python train.py
    python train.py --epochs 30 --lr 5e-5
"""
import argparse

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

import config
from dataset import (
    CrystalDataset,
    load_valid_dataset,
    split_dataset,
    split_dataset_by_folder,
    test_transform,
    train_transform,
)
from model import build_model


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset-csv", type=str, default=str(config.DATASET_CSV))
    p.add_argument("--model-path", type=str, default=str(config.MODEL_PATH))
    p.add_argument("--epochs", type=int, default=config.EPOCHS)
    p.add_argument("--lr", type=float, default=config.LR)
    p.add_argument("--batch-size-train", type=int, default=config.BATCH_SIZE_TRAIN)
    p.add_argument("--batch-size-test", type=int, default=config.BATCH_SIZE_TEST)
    p.add_argument("--num-workers", type=int, default=config.NUM_WORKERS)
    p.add_argument("--split-mode", choices=["random", "folder"], default="random",
                    help="random: 結晶単位のランダム分割(従来通り)。"
                         "folder: 実験回(source_folder)単位で分割し、未知の回への汎化を検証する。")
    p.add_argument("--train-split-csv", type=str, default=str(config.TRAIN_SPLIT_CSV),
                    help="train split の保存先。split-mode=folderで検証するときは、"
                         "既存のtrain_split.csv/test_split.csvを上書きしないよう別名を指定すること。")
    p.add_argument("--test-split-csv", type=str, default=str(config.TEST_SPLIT_CSV))
    return p.parse_args()


def main():
    args = parse_args()
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_amp = device.type == "cuda"
    print(f"デバイス: {device}  (AMP: {use_amp})")

    df_all = load_valid_dataset(args.dataset_csv)
    if args.split_mode == "folder":
        train_df, test_df = split_dataset_by_folder(df_all)
    else:
        train_df, test_df = split_dataset(df_all)
    train_df.to_csv(args.train_split_csv, index=False, encoding="utf-8-sig")
    test_df.to_csv(args.test_split_csv, index=False, encoding="utf-8-sig")

    train_loader = DataLoader(CrystalDataset(train_df, train_transform),
                               batch_size=args.batch_size_train, shuffle=True,
                               num_workers=args.num_workers, pin_memory=True,
                               persistent_workers=args.num_workers > 0)
    test_loader = DataLoader(CrystalDataset(test_df, test_transform),
                              batch_size=args.batch_size_test, shuffle=False,
                              num_workers=args.num_workers, pin_memory=True,
                              persistent_workers=args.num_workers > 0)

    model = build_model().to(device)
    criterion = nn.HuberLoss(delta=1.0)
    mse_fn = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=config.WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=3)
    scaler = torch.amp.GradScaler(device.type, enabled=use_amp)

    best_mse = float("inf")
    for ep in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device).unsqueeze(1)
            optimizer.zero_grad()
            with torch.amp.autocast(device.type, enabled=use_amp):
                loss = criterion(model(x), y)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            scaler.step(optimizer)
            scaler.update()
            total_loss += loss.item() * x.size(0)
        train_mse = total_loss / len(train_df)

        model.eval()
        t_mse = t_mae = 0.0
        with torch.no_grad():
            for x, y in test_loader:
                x, y = x.to(device), y.to(device).unsqueeze(1)
                with torch.amp.autocast(device.type, enabled=use_amp):
                    out = model(x)
                t_mse += mse_fn(out, y).item() * x.size(0)
                t_mae += (out - y).abs().sum().item()
        test_mse = t_mse / len(test_df)
        test_mae = t_mae / len(test_df)

        scheduler.step(test_mse)
        tag = ""
        if test_mse < best_mse:
            best_mse = test_mse
            torch.save(model.state_dict(), args.model_path)
            tag = "  ← best 保存"
        print(f"Epoch {ep:2d}: train={train_mse:.4f}  test={test_mse:.4f}  MAE={test_mae:.4f} µm{tag}")

    print(f"\n学習完了。best test MSE = {best_mse:.4f}")


if __name__ == "__main__":
    main()
