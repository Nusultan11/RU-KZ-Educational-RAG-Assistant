# Kazakh Retrieval EDA Findings

## Dataset

- Name: `shyngys879/Kazakh-Wiki-RAG-Dataset`
- Role: Kazakh retrieval corpus
- Stage: Retrieval EDA findings report

## Current Status

EDA notebook: `notebooks/eda_kaz_corpus_rag.ipynb`.

The notebook inspected the dataset CSV structure and triplet fields. No preprocessing, chunking, embeddings, indexing, RAG, or QLoRA were performed.

## Findings

### Sizes

Measured:

- `train.csv`: `17,320` rows, `3` columns;
- `train_pairs.csv`: `17,320` rows, `3` columns;
- `train_triplets.csv`: `17,320` rows, `4` columns.

### Columns

Confirmed columns:

- train: `anchor`, `positive`, `source`;
- pairs: `anchor`, `positive`, `source`;
- triplets: `anchor`, `positive`, `negative`, `source`.

### Duplicates

Measured on triplets:

- duplicate `anchor`: `0`;
- duplicate `positive`: `0`;
- duplicate `negative`: `6,119`.

Negative duplicates are high and should be reviewed before training or evaluation logic uses negatives.

### Lengths

Measured on triplets:

- `anchor` mean: `38.40`, p50: `38`, p75: `45`, p90: `53`, p95: `59`, p99: `72`, max: `114`;
- `positive` mean: `354.96`, p50: `306`, p75: `507`, p90: `607`, p95: `629`, p99: `646`, max: `650`;
- `negative` mean: `353.47`, p50: `306`, p75: `503`, p90: `605`, p95: `629`, p99: `646.81`, max: `650`.

### Retrieval Readiness

Status: partially ready.

The dataset contains explicit `anchor`, `positive`, and `negative` fields in triplets. This is useful for retrieval training/evaluation design, but the high number of duplicate negatives must be handled carefully.

## Conclusions

- Kazakh retrieval schema is clear: anchor-positive pairs and anchor-positive-negative triplets exist.
- Positive examples are not duplicated in the measured triplet table.
- Negative examples have `6,119` duplicates and need review.
- Positive/negative passages are capped around `650` characters, which is useful evidence for future chunking decisions.
- No preprocessing or RAG tuning should start until a data quality report defines filtering rules.

## Open Questions

1. Are there validation/test splits, or only train CSV files?
2. Are `source` values stable enough for citations?
3. Why are negative passages heavily duplicated?
4. Should duplicate negatives be removed or downweighted?
5. Should Kazakh retrieval use a separate index or shared multilingual index?

## Next Step

Run a scoped EDA script that records schema, splits, row counts, text length distributions, language distribution, and whether explicit relevance labels exist.
