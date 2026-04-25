# Module 1: Input Packing and Normalization

Choose one input-packing strategy.

## `raw_stack_shared_norm`

- Pack `RGB@t1` and `SAR@t2` into one raw 5-channel tensor
- Apply a shared normalization path before later processing

## `separate_norm_then_concat`

- Normalize RGB and SAR with separate statistics
- Concatenate the resulting tensors into one merged tensor before later processing

## `separate_stream_pack`

- Keep RGB and SAR as separate streams
- Do not form one merged input tensor at the packing stage
