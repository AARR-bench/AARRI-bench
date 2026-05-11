Hi Fatima,

This looks like a memory leak in the gradient computation rather than a static sizing issue (since it crashes after step 47, not step 1). The growing memory usage is the key clue.

Try these in order:
1. Enable gradient checkpointing: model.gradient_checkpointing_enable() — this trades compute for memory.
2. Use 8-bit AdamW from bitsandbytes — the optimizer states (which are large) are stored in 8-bit.
3. If you're accumulating a computation graph without calling .detach() on things that don't need gradients, that would cause this.
4. Check if you're storing any tensors in a Python list/dict between batches — these prevent garbage collection.

The gradual growth pattern strongly suggests option 3 or 4.
