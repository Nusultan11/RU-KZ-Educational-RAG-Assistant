# Data Flow

## Offline Pipeline

The offline pipeline prepares knowledge and evaluation artifacts.

```text
dataset inventory
  -> EDA
  -> data quality report
  -> preprocessing plan
  -> preprocessing
  -> chunking
  -> embeddings
  -> vector index
  -> evaluation datasets
```

## Online Pipeline

The online pipeline answers a user question.

```text
user question
  -> language detection
  -> query normalization
  -> index selection
  -> top-k retrieval
  -> optional reranking
  -> context building
  -> prompt building
  -> LLM generation
  -> response validation
  -> answer with sources
```

## Data Contracts

### Document

- `id`: stable document id
- `language`: `ru`, `kk`, or another detected code
- `title`: optional title
- `text`: source text
- `source`: source reference
- `metadata`: additional source metadata

### Chunk

- `id`: stable chunk id
- `document_id`: parent document id
- `language`: chunk language
- `title`: optional title
- `text`: chunk text
- `source`: source reference
- `chunk_index`: chunk order inside document
- `metadata`: chunk metadata

### RetrievalResult

- `chunk_id`: matched chunk id
- `text`: retrieved text
- `score`: retrieval score
- `language`: result language
- `source`: source reference
- `metadata`: result metadata

### RAGResponse

- `answer`: final answer
- `language`: answer language
- `sources`: cited retrieval results
- `confidence`: optional confidence estimate
- `metadata`: runtime metadata

## Guardrails

- Raw data must not be modified in place.
- Preprocessing decisions must be justified by EDA.
- Evaluation splits must remain fixed for comparisons.
- Generated artifacts should be versioned or reproducible from config.

