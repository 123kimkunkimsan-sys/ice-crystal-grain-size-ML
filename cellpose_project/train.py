"""Cellposeの追加学習(ファインチューニング)スクリプト(骨組みのみ、未実装)。

ゴール: 汎用学習済みモデル(例: "cyto3")を出発点に、prepare_dataset.py で用意した
氷結晶データで追加学習し、結晶のインスタンスマスクを予測できるようにする。

TODO:
1. まずは学習済みモデルを無調整で試す(train.pyを書く前に、手元の画像数枚に対して
   `cellpose --use_gpu --pretrained_model cyto3 --dir <画像フォルダ>` をCLIで実行し、
   どの程度拾えるか目視確認するのが最初の一歩)。
2. 無調整では不十分な場合、Cellpose Python APIで追加学習する:
   from cellpose import models, io
   model = models.CellposeModel(gpu=True, pretrained_model="cyto3")
   model.train(train_data, train_labels, ...)
   公式ドキュメント: https://cellpose.readthedocs.io/en/latest/train.html
3. 学習後、推論結果(マスク)から円相当径を計算する関数を書く:
   d_um = sqrt(4 * (マスクの画素数 * um_per_pixel**2) / pi)
   (inference/validate_unseen.ipynb の NEW_MAG_TO_UM_PER_PIXEL と同じ校正値を使うこと)
4. 既存の inference/validate_unseen.ipynb と同じ-12℃未知データ・同じGT CSVで評価し、
   ②③④の指標(R², RMSE, MAE)を既存パイプラインと比較する。
"""

raise NotImplementedError("骨組みのみ。まずは学習済みモデルの無調整テストから始める。")
