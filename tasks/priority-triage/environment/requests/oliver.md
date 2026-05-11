**From:** Oliver Kim
**To:** Advisor
**Date:** January 14, 2025, 3:02 PM
**Subject:** Quick question — Adam vs Muon optimizer

---

Hey,

Hope you're having a good week. Quick question when you get a chance — no rush at all.

I'm starting to think about which optimizer to use for the next phase of my pretraining experiments. I've been using AdamW pretty much by default, but I've been seeing a lot of discussion about Muon recently (Kosson et al., the orthogonal gradient update thing). Karpathy mentioned it in a tweet and there's been some chatter on Twitter/X about it being significantly better for transformers.

From what I can tell, Muon applies Nesterov momentum in the "steepest descent" sense under the spectral norm (instead of L2), which should in theory be better matched to the geometry of weight matrices. But I'm not sure how much of the claimed improvement carries over to settings outside of small-scale experiments.

My setup: 350M parameter transformer language model, training on ~50B tokens of text, single node 8x H100. Nothing exotic.

The practical concerns I have:
1. Muon is less mature software-wise — fewer battle-tested implementations
2. Not sure if the gains generalize to this scale (most comparisons I've seen are on smaller models)
3. If something goes wrong, AdamW has much better community support for debugging

On the other hand, if Muon is genuinely 10-20% more compute-efficient for the same loss, that's a meaningful difference at 50B tokens.

Do you have any thoughts on this? I'm happy to just stick with AdamW if you think the marginal gain isn't worth the risk of using a less established optimizer. Either way, not a blocker for me — I can start the run with AdamW and revisit if needed.

Thanks,
Oliver
