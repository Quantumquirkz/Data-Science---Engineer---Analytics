# Big Data And Cloud Patterns

This module introduces the architectural ideas behind large-scale data systems
without forcing the repository to become cloud-dependent. The emphasis is on
partitioning, file formats, distributed thinking, orchestration boundaries, and
cost-aware design.

## Learning Outcomes

After this module, a learner should be able to:

- explain when pandas is enough and when a larger processing model is needed;
- describe partitioning by time, entity, or domain key;
- distinguish row-oriented and columnar storage tradeoffs;
- reason about batch, streaming, and incremental processing;
- identify bottlenecks in I/O, memory, network movement, and recomputation;
- design a cloud-ready pipeline while keeping local samples reproducible.

## Scaling Model

```mermaid
flowchart LR
    sample["Local sample"] --> batch["Batch processing"]
    batch --> partition["Partitioned datasets"]
    partition --> orchestration["Orchestration"]
    orchestration --> monitoring["Quality and cost monitoring"]
    monitoring --> backfill["Backfill or incremental update"]
```

## Core Concepts

- **Columnar storage**: efficient analytical scans over selected columns.
- **Partitioning**: physical organization that reduces unnecessary reads.
- **Batch processing**: scheduled transformation over bounded data.
- **Streaming**: processing unbounded events with latency constraints.
- **Backfill**: recomputing historical outputs when logic or source data changes.
- **Cost model**: storage, compute, transfer, orchestration, and human
  maintenance cost.

## Practice Sequence

1. Take a small CSV and define a larger logical dataset around it.
2. Decide a partitioning key and justify it.
3. Write row-count and null-rate checks for each processing stage.
4. Sketch a DAG with ingestion, validation, transform, publish, and monitoring.
5. Explain which parts can run locally and which would move to cloud later.

## References

- Apache Airflow core concepts:
  https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html
- Apache Airflow DAGs:
  https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html

## Projects

- `p039` [Large-Scale Astronomy Catalog Linker](../../../projects/large_scale_astronomy_catalog_linker/README.md) -
  entity resolution and catalog-scale joins.
- `p040` [Large-Scale Log Compression and Analytics](../../../projects/large_scale_log_compression_and_analytics/README.md) -
  log analytics and compression-aware pipeline thinking.
- `p043` [Large-Scale Text Mining of Scientific Literature](../../../projects/large_scale_text_mining_of_scientific_literature/README.md) -
  document-scale processing.
- `p076` [Scientific Data Platform for Multi-Modal Experiments](../../../projects/scientific_data_platform_for_multi_modal_experiments/README.md) -
  platform-oriented data integration.

## Assessment Pattern

A learner should be able to explain the problem framing, run the notebook or pipeline, inspect the outputs, and state the limitations.
