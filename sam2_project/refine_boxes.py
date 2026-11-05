"""YOLOのボックス検出をSAM2で精緻化し、マスク面積から円相当径を計算する(骨組みのみ、未実装)。

学習は不要(SAM2はゼロショットでボックスプロンプトに対応)。まずは少数の画像で
目視確認してから、inference/validate_unseen.ipynb 相当の検証に展開する想定。

TODO:
1. inference/validate_unseen.ipynb の get_pred_boxes_and_diameters 相当のロジックで、
   既存のYOLOv8(+SAHI)検出を流用し、ボックス一覧を得る(ResNetの回帰呼び出しは行わない)。
2. SAM2をロードし、各ボックスをプロンプトとして渡してマスクを得る:
   from sam2.sam2_image_predictor import SAM2ImagePredictor
   predictor = SAM2ImagePredictor(sam2_model)
   predictor.set_image(image)
   mask, score, _ = predictor.predict(box=box, multimask_output=False)
   公式ドキュメント: https://github.com/facebookresearch/sam2
3. マスクの画素数から円相当径を計算する:
   d_um = sqrt(4 * (マスクの画素数 * um_per_pixel**2) / pi)
   (inference/validate_unseen.ipynb の NEW_MAG_TO_UM_PER_PIXEL と同じ校正値を使うこと)
4. 既存の②ResNet単体・③パイプライン全体と同じ条件(同じ-12℃未知データ、同じGT CSV)で
   比較する。「ボックスは同じでもマスク面積の方が正確か」を確認するのがこの検証の目的。
"""

raise NotImplementedError("骨組みのみ。まずはSAM2単体の目視テストから始める。")
