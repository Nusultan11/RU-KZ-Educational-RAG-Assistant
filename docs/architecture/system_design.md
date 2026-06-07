# System Design

## Goal

Build a production-oriented LLM + RAG educational assistant for Russian and Kazakh languages.

The system must support reliable retrieval, grounded answers with sources, language-aware behavior, measurable quality, and future deployment.

## Architecture Principle

The project is split into independent layers:

```text
Project Control
  -> Data + EDA
  -> Preprocessing
  -> Indexing
  -> Retrieval
  -> Generation
  -> Evaluation
  -> API / UI
  -> Monitoring / Feedback
```

No single module should mix loading, preprocessing, retrieval, generation, and evaluation.

## Layers

| Layer | Responsibility |
| --- | --- |
| `core` | Configuration, logging, exceptions, registries |
| `data` | Dataset loading contracts, schemas, validation |
| `eda` | Profiling, statistics, language analysis, quality checks |
| `preprocessing` | Cleaning, normalization, deduplication, language filtering, chunking |
| `indexing` | Embedding and vector-store interfaces |
| `retrieval` | Query processing, language routing, search, reranking, context building |
| `generation` | Prompt building, LLM boundary, answer validation, citations |
| `evaluation` | Retrieval, RAG, generation metrics, error analysis |
| `training` | Future retriever fine-tuning and QLoRA planning |
| `api` | Future service endpoints |
| `monitoring` | Logs, feedback, traces |

## Required Gates

- EDA before preprocessing.
- Baseline RAG before improvements.
- Retrieval evaluation before RAG tuning.
- RAG evaluation and error analysis before QLoRA.
- Explicit report after every major step.

## Current Implementation State

This document describes the intended architecture. The current skeleton intentionally contains no business logic.

