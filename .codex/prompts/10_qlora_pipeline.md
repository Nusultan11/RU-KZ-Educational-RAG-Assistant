# QLoRA Pipeline Prompt

Use this prompt only after the required RAG and evaluation gates are complete.

## Entry Gate

QLoRA is allowed only after:

- baseline RAG exists;
- EDA is complete;
- preprocessing is complete;
- retrieval evaluation is complete;
- RAG evaluation is complete;
- error analysis shows a fine-tuning need.

If any item is missing, stop and propose the missing prerequisite step.

## Required Justification

Before planning fine-tuning, explain:

- why fine-tuning is needed;
- which specific failure mode it solves;
- why prompt engineering, RAG changes, or reranking are insufficient;
- which data will be used;
- whether the data is licensed and clean enough;
- how training data will be separated from evaluation data.

## Required Training Plan

Document:

- instruction data format;
- base model;
- max sequence length;
- LoRA target modules;
- rank, alpha, dropout;
- quantization settings;
- batch size and gradient accumulation;
- learning rate and scheduler;
- evaluation metrics;
- base-vs-fine-tuned comparison;
- rollback plan.

## Prohibitions

- Do not start training from root mode.
- Do not use unvalidated data.
- Do not report improvement without held-out evaluation.

