# Module 3: Integration with YOLO and Pretraining

Choose one strategy for handling the existing RGB-pretrained backbone.

## `widen_rgb_stem`

- Expand the existing RGB stem so it can receive more channels directly

## `replace_with_new_shared_stem`

- Discard the current RGB-pretrained stem
- Introduce a new shared stem for the combined setting

## `keep_rgb_stem_plus_sar_adapter`

- Retain the RGB-pretrained stem
- Add a separate SAR adapter path before later fusion
