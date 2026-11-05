"""StarDistの学習スクリプト(骨組みのみ、未実装)。

TODO:
1. prepare_dataset.py で用意した画像・ラベルのペアを読み込む。
2. StarDist2Dモデルを作成し学習する:
   from stardist.models import StarDist2D, Config2D
   model = StarDist2D(Config2D(...), name="ice_crystal_stardist", basedir="models")
   model.train(X_train, Y_train, validation_data=(X_val, Y_val), ...)
   公式チュートリアル: https://github.com/stardist/stardist/blob/main/examples/2D/2_training.ipynb
3. 学習後、推論結果(ポリゴン)から円相当径を計算する関数を書く:
   d_um = sqrt(4 * (ポリゴン面積 * um_per_pixel**2) / pi)
   (inference/validate_unseen.ipynb の NEW_MAG_TO_UM_PER_PIXEL と同じ校正値を使うこと)
4. 既存の inference/validate_unseen.ipynb と同じ-12℃未知データ・同じGT CSVで評価し、
   ②③④の指標(R², RMSE, MAE)を既存パイプライン・他候補(Cellpose等)と比較する。
"""

raise NotImplementedError("骨組みのみ。prepare_dataset.py の完成が先。")
