# Sentiment Model Comparison (Test Set, n=5385)

Binary classification: Negative (222 samples) / Positive (5163 samples).

## Metrics

| Model | Accuracy | Macro F1 | Negative F1 | Positive F1 |
|---|---|---|---|---|
| cardiffnlp-twitter | 99.07% | 0.939 | 0.883 | 0.995 |
| roberta | 99.05% | 0.937 | 0.879 | 0.995 |
| bert | 98.96% | 0.932 | 0.869 | 0.995 |
| distilbert | 98.87% | 0.928 | 0.862 | 0.994 |
| nlptown-multilingual | 98.64% | 0.911 | 0.830 | 0.993 |

## Confusion matrices

| Model | Neg→Neg | Neg→Pos | Pos→Neg | Pos→Pos |
|---|---|---|---|---|
| cardiffnlp-twitter | 189 | 33 | 17 | 5146 |
| roberta | 186 | 36 | 15 | 5148 |
| bert | 186 | 36 | 20 | 5143 |
| distilbert | 190 | 32 | 29 | 5134 |
| nlptown-multilingual | 178 | 44 | 29 | 5134 |

## Takeaway

`cardiffnlp-twitter` ranks best on macro F1 and catches the most true Negatives
(189/222), making it the best default choice for the API given the class
imbalance in this dataset. `nlptown-multilingual` is the weakest — its
pretrained head/tokenizer (5-star, multilingual) transfers less well to this
binary English task than the general-purpose or Twitter-pretrained models.
