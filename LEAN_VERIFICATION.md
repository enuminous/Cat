# Shared Lean 4 verification for Cat

The selected formal core is maintained in the shared [Monolithic Zoo package](https://github.com/enuminous/Monolithic-Zoo-Lean4).

- Checked module: [Cat.lean](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/44d9881e8878a702fdfa47da53d80436276d92a6/Cat.lean).
- Verified package commit: `44d9881e8878a702fdfa47da53d80436276d92a6`.
- Successful workflow: [38484522045](https://github.com/enuminous/Monolithic-Zoo-Lean4/actions/runs/38484522045).
- Selected upstream source revision: [`9bf56f891b3ac22e38089ade0351852df1670d11`](https://github.com/enuminous/Cat/commit/9bf56f891b3ac22e38089ade0351852df1670d11); preserved source blobs and hashes are in the shared package's `UPSTREAM_SOURCES.json`.
- Scope: ablation penalty and sign classifier; exact-integer sign reference.
- Named theorem declarations: `Zoo.Cat.positive_removal_hurt`, `Zoo.Cat.removal_hurts_iff`.

The run passed the pinned Lean build, strict axiom audit, audit rejection controls,
90 finite reference comparisons across the shared package, and the 46-module roster.
These are package-level checks; they do not mean that 90 tests belong to this animal.

This evidence covers the selected core and its stated hypotheses. It does not
certify this repository's complete Python pipeline, feature extraction, training,
all floating-point edge cases, or empirical effectiveness. The shared
[coverage ledger](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/COVERAGE.md)
and [remaining obligations](https://github.com/enuminous/Monolithic-Zoo-Lean4/blob/main/FORMALIZATION_NOTES.md)
preserve those limits. Future source changes require a fresh correspondence review.

Reuse the pinned shared package instead of maintaining a divergent proof copy here.
