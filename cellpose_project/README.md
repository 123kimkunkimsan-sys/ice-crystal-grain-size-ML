# Cellpose候補ブランチ(骨組みのみ)

## これは何か

既存パイプライン(YOLOv8でボックス検出 → ResNet18で直径回帰)の根本的なボトルネックは、
「YOLOのボックスがタイトでない」「大型・複雑形状の結晶を検出し損ねる」という、
**ボックスベース検出そのものの弱さ**であることが、`inference/validate_unseen.ipynb`での
-12℃未知データ検証で繰り返し確認された(ResNet単体は改善してもパイプライン全体・k値は改善せず)。

Cellposeは、ボックスではなく**インスタンスセグメンテーション**(1結晶ごとのピクセル単位マスク)
を直接予測する手法。GTの「円相当径」はもともと面積(セグメンテーション)起源の指標なので、
ボックス経由で近似するより、素直にマスク面積から直径を計算する方が理屈に合っている。

## なぜCellposeを選んだか

1. **氷結晶での直接の前例がある**: Saad et al., "A novel automated protocol for ice crystal
   segmentation analysis using Cellpose and Fiji," *Cryobiology* 111 (2023) 1–8.
   (DOI: 10.1016/j.cryobiol.2023.02.002)
   再結晶化阻害アッセイの氷結晶画像に対してCellposeを使い、1画像あたり約70秒で結晶ごとに
   セグメンテーションしたと報告。本研究と非常に近いタスク設定。
2. **汎用学習済みモデル + 人間参加型の追加学習**: Stringer et al., "Cellpose: a generalist
   algorithm for cellular segmentation," *Nature Methods* 18 (2021) 100–106.
   (https://www.nature.com/articles/s41592-020-01018-x)
   勾配フロー予測によるセグメンテーションで、接触・重なった物体の分離に強い。GUIで
   「予測結果を手で修正→再学習」のループが組まれており、機械学習の専門知識がなくても
   ラベル付けと追加学習がしやすい設計になっている(野中さんのように非情報系の研究者でも
   扱いやすいのが大きな利点)。
3. 発展版として、サイズばらつきの大きい結晶に特化したマルチスケール注意機構を追加する
   研究もある: Neubauer et al., "Multi-scale attention-based instance segmentation for
   measuring crystals with large size variation," arXiv:2401.03939 (2024)。
   Cellposeをベースに、サイズのばらつきが大きい結晶(=本研究の弱点そのもの)に対応する
   改良を加えている。Cellposeでうまくいかない場合の次の一手として参考になる。

## 既存パイプラインとの関係(統合イメージ)

- YOLOv8による検出ステップを置き換える(または並行して試す)。
- ResNet18による直径回帰は不要になる可能性が高い: セグメンテーションマスクの面積から
  直接「円相当径」を計算できるため(`d = sqrt(4 * area / pi)`、GTの定義と完全に一致)。
- 既存の`inference/validate_unseen.ipynb`と同じ-12℃未知データで、同じGT CSVを使って
  検証できる(比較のハードルを揃えやすい)。

## 未解決の課題(要検討)

- **マスクのラベルがない**: 現状のCSVは矩形(ボックス)+円相当径+円形度のみで、ピクセル単位の
  マスクは存在しない。Cellposeの学習には最低限のマスクラベルが必要。
  - 案1: 既存ボックス内で単純な二値化(大津の閾値処理など)を行い、仮マスクを自動生成して
    学習の出発点にする(`pixel_baseline.py`の`pixelcount`手法が近い考え方)。
  - 案2: Cellposeの汎用学習済みモデル(`cyto3`など)をまず無調整で試し、結果が良ければ
    ラベル付けコストをかけずに使える可能性がある(ゼロショットに近い使い方)。
  - 案3: 少数の画像だけ手動でマスクを修正し(CellposeのGUIで補正)、そこから追加学習する。
- -6℃と-12℃でカメラの色味・解像度が異なる問題は、Cellposeでも同様に起こりうる。
  既存パイプラインで確立した「グレースケール化」「スケール補正」の前処理は、ここでも
  踏襲すべき。
- 大型・複雑形状の結晶をCellposeがどこまで拾えるかは未検証。既存の弱点(学習データに
  30µm以上の例が少ない)が、ここでも別の形で出る可能性はある。

## 参考リンク

- Cellpose公式: https://github.com/MouseLand/cellpose
- Stringer et al. 2021 (Nature Methods): https://www.nature.com/articles/s41592-020-01018-x
- Saad et al. 2023 (Cryobiology, 氷結晶への直接適用): DOI 10.1016/j.cryobiol.2023.02.002
- Neubauer et al. 2024 (サイズばらつき対応の発展版): https://arxiv.org/abs/2401.03939
