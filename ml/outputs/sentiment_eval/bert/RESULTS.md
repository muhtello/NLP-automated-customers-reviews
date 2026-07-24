# Sentiment Model — Results (Held-out Test Set)

## Design decision: 2-class, not 3-class

The README's default mapping is 1-2 = Negative, 3 = Neutral, 4-5 = Positive. We dropped
the Neutral (3-star) class entirely rather than training on it (`ml/src/data_cleaning/clean.py`,
`RATING_TO_SENTIMENT`). 3-star review text is frequently ambiguous — it mixes praise and
complaints in the same sentence — and is a small, noisy slice of the data. Rather than
force a transformer to learn a fuzzy boundary from limited, low-quality examples, we scoped
the model to the two classes with clear textual signal: Negative and Positive. This is an
intentional simplification, not an oversight, and it costs Neutral-nuance detection in
exchange for materially cleaner Negative/Positive performance.

## Overall accuracy

**98.98%** on 5,385 held-out test reviews.

Accuracy alone is misleading here — the test set mirrors the ~69%-Positive skew in the raw
data (5,163 Positive vs 222 Negative), so a model that always predicts Positive would still
score ~95.9%. Macro F1 is the metric that matters for this dataset.

## Per-class metrics

| Class | Precision | Recall | F1-score | Support |
|---|---|---|---|---|
| Negative | 89.6% | 85.1% | 87.3% | 222 |
| Positive | 99.4% | 99.6% | 99.5% | 5,163 |
| **Macro avg** | **94.5%** | **92.4%** | **93.4%** | 5,385 |

## Confusion matrix

|  | Predicted Negative | Predicted Positive |
|---|---|---|
| **Actual Negative** | 189 | 33 |
| **Actual Positive** | 22 | 5,141 |

(Visual: `confusion_matrix.png` in this directory.)

## Interpretation

- The model is near-perfect on Positive reviews (99%+ across the board) — expected, given
  Positive examples dominate training data by roughly 23:1.
- The weak point is Negative recall (85.1%): 33 of 222 genuinely negative reviews were
  misclassified as Positive. Class weighting (`WeightedTrainer`, inverse-frequency loss
  weights) was applied during training specifically to counter this imbalance, and macro-F1
  (not accuracy) was used as the model-selection metric — without these, Negative recall
  would likely be worse.
- Manual UI testing surfaced a concrete failure mode consistent with this: mixed-sentiment
  sentences with price complaints (e.g. "My son bought this and he loves it. And it's too
  expensive!") are predicted Positive with very high confidence (99.9%). Root-cause analysis
  of the training data showed why: of 1,157 training reviews containing the word
  "expensive," 96.5% are labeled Positive — mostly "in**expensive**" or favorable price
  comparisons ("less expensive than X"), not complaints. The model correctly learned this
  dataset-level correlation, but it means genuine price complaints are a documented blind
  spot rather than a bug to patch.
- Takeaway: overall accuracy looks excellent, but the honest read is macro F1 = 93.4%, with
  Negative-class recall as the model's known weakness — driven by both class imbalance and
  a training corpus that rarely contains genuine price-complaint negatives.
