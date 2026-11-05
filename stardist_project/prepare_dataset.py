"""StarDist用データセット準備(骨組みのみ、未実装)。

cellpose_project/prepare_dataset.py と基本的な考え方は同じ(マスクが必要)。
StarDistは入力に「画像 + ラベル画像(結晶ごとに異なる整数値を割り当てたもの)」を
使う点はCellposeとほぼ共通。

TODO:
1. 元画像と矩形ラベルCSVを読み込む(colab/crystal_dataset_pipeline.ipynb や
   inference/validate_unseen.ipynb の get_gt_boxes_diameters_circularity 相当のロジックを流用)。
2. マスク生成方法を決める(README「未解決の課題」、cellpose_project/README.md の
   案1〜3を参照。StarDistでも同様の制約がある)。
3. StarDistが期待する形式(画像配列 + 同サイズのラベル配列のペアのリスト)に変換する。
   公式チュートリアル: https://github.com/stardist/stardist/tree/main/examples
4. train/val split を画像単位で行う(パッチ単位で分けるとリークするので注意。
   vscode_project/dataset.py の split_dataset() と同じ考え方)。

導入前の確認事項(README参照): 大型・複雑形状の結晶がstar-convexの前提から
どの程度外れているか、まず数枚の画像で目視確認すること。
"""

raise NotImplementedError("骨組みのみ。マスク生成方法と形状の前提確認が先。")
