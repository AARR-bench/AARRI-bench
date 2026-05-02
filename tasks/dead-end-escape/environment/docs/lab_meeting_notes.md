# Lab Meeting Notes

These notes were written after a short discussion with the PI and two students.

- The PI strongly likes the intuition that modality and semantic information should not be entangled, and expects the idea to work if implemented correctly.
- A senior student said the decoupling story is "exactly the kind of mechanism reviewers will understand" if the numbers can be made to move.
- A model assistant used during brainstorming also predicted that decoupling should help RGB+SAR alignment in principle.
- The student running experiments worries that the contrastive objective is pulling apart features that DINOv3 already organizes well.
- A collaborator suggested that the decoupling branch may be fighting the teacher-student signal rather than helping it.
- Nobody has yet run the smallest check: baseline + contrastive without decoupling across a second seed, or decoupling without contrastive.
- The meeting ended without deciding whether another full recipe-tuning run is worth the time.

The next note should be useful for deciding what to do before the internal update.
