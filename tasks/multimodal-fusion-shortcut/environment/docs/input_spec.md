# Input Specification

The revised project uses two aligned streams per sample:

- `RGB@t1`: a standard 3-channel optical image collected at the earlier timestamp
- `SAR@t2`: a 2-channel SAR observation collected at the later timestamp

Important implications:

- The two inputs do not share the same channel semantics.
- The two inputs do not come from the same timestamp.
- A raw channel stack would create a single 5-channel tensor, but that representation would hide which information comes from the earlier RGB view and which comes from the later SAR view.

Design requirements derived from the input definition:

- preserve which stream is earlier and which stream is later
- preserve the fact that RGB and SAR have different statistics
- avoid unnecessary changes to the RGB-pretrained stem unless the gain clearly outweighs the cost
