Hi David,

The epoch-consistent NaN behavior strongly suggests gradient explosion. The fact that it happens at the same epoch (not random) and that gradient clipping helped slightly (but didn't fix it) points to a specific cause.

Most likely issue: your learning rate is too high relative to the model's loss landscape at epoch 4. As loss decreases, the gradients can become sharper and more prone to explosion. Try:
1. Reduce lr further to 1e-6
2. Add learning rate warmup (first 1000 steps)
3. Reduce max_norm in gradient clipping to 0.1

Also check: are you accumulating gradients without zeroing them between batches? That would cause exactly this behavior.
