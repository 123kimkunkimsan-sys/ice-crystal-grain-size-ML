"""Cellpose用データセット準備(骨組みのみ、未実装)。

ゴール: 既存のボックス+円相当径CSV(例: vscode_project/data/dataset.csv 相当の元データ)から、
Cellposeが学習に使える「画像 + インスタンスマスク(各結晶に別IDを振った整数ラベル画像)」の
ペアを作る。

TODO:
1. 元画像と矩形ラベルCSVを読み込む(colab/crystal_dataset_pipeline.ipynb や
   inference/validate_unseen.ipynb の get_gt_boxes_diameters_circularity 相当のロジックを流用)。
2. マスクをどう作るか決める(README「未解決の課題」案1〜3を参照)。
   最初のステップとしては、各矩形内で大津の二値化を行い、仮マスクを自動生成するのが
   手早く始められる(vscode_project/pixel_baseline.py の pixelcount_diameter_um 関数が近い処理)。
3. Cellposeが期待する形式で保存する:
   - 画像: images/<name>.png
   - マスク: images/<name>_masks.png (同じ画像に写る結晶ごとに 1, 2, 3, ... の整数ラベル)
   参考: https://cellpose.readthedocs.io/en/latest/io.html
4. train/val split を作る(画像単位で分割すること。vscode_project/dataset.py の
   split_dataset() と同じ考え方で、パッチ単位ではなく元画像単位で分けてリークを防ぐ)。
"""

raise NotImplementedError("骨組みのみ。マスク生成方法(README参照)を決めてから実装する。")
