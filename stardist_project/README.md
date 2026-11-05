# StarDist候補ブランチ(骨組みのみ)

## これは何か

セミ中の雑談で出た「仮説②」そのもの。ボックスではなく、各結晶を**星型凸多角形
(star-convex polygon)**として直接予測するインスタンスセグメンテーション手法。
中心点から放射状に伸びる距離を密に予測し、non-maximum suppressionでインスタンスを
確定する。GTの円相当径は面積起源の指標なので、ボックス経由より筋が良い、という
発想はCellposeと同じ。

## なぜ候補に残したか・優先度について

- Schmidt et al., "Cell Detection with Star-convex Polygons," MICCAI 2018
  (arXiv:1806.03535, https://arxiv.org/abs/1806.03535)。細胞核のセグメンテーション用に
  開発され、顕微鏡画像の粒状オブジェクト検出で広く使われている定番手法。
- 3D拡張版: Weigert et al., "Star-convex Polyhedra for 3D Object Detection and
  Segmentation in Microscopy," WACV 2020 (arXiv:1908.03636)。
- **正直な評価として、今回はCellposeを優先候補にした。** 理由:
  1. Cellposeには氷結晶への直接適用例(Saad et al. 2023, Cryobiology)があるが、
     StarDistには見当たらなかった。
  2. StarDistは「星型凸(star-convex)」という形状の前提を置いている。小さく比較的
     丸い結晶には向いているはずだが、本研究で一番困っている「大型・複雑形状
     (細長い・非凸な)結晶」は、この前提に合わない可能性がある。星型凸でない形状は
     本質的にうまく表現できないため、むしろ最大の課題である大型結晶でこそ弱さが
     出るおそれがある。
  3. Cellposeは勾配フロー方式で、接触・非凸形状への対応がより柔軟とされる。
  
  とはいえStarDistは実装が軽く、顕微鏡画像での実績も豊富なので、Cellposeで
  思うような結果が出なかった場合の代替・比較対象として残す価値はある。

## 既存パイプラインとの関係(統合イメージ)

- Cellpose案と同様、YOLOv8の検出ステップを置き換え、ResNetの回帰も不要にする狙い。
- マスク(ポリゴン)面積から円相当径を直接計算する。

## 未解決の課題(要検討)

- **マスクのラベルがない**(Cellpose案と同じ制約。cellpose_project/README.mdの
  案1〜3を参照)。
- **星型凸の前提**: 本研究で最も精度が落ちている「大型・複雑形状の結晶」こそ、
  この前提から外れやすい。導入前に、実際の大型結晶の形状がどの程度star-convexから
  外れているか、サンプル画像で目視確認すべき。
- -6℃/-12℃のカメラ間の色味・解像度差への対応は、既存パイプラインで確立した
  前処理(グレースケール化・スケール補正)をここでも踏襲する。

## 補足: 依存ライブラリについて

StarDistはTensorFlow(Keras)ベースで、本リポジトリの他の部分(PyTorch)とは別の
フレームワーク。`requirements.txt`も専用の仮想環境を分けて使うことを想定している。

## 参考リンク

- StarDist公式: https://github.com/stardist/stardist
- Schmidt et al. 2018 (MICCAI, 2D): https://arxiv.org/abs/1806.03535
- Weigert et al. 2020 (WACV, 3D拡張): https://arxiv.org/abs/1908.03636
