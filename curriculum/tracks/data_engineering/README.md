# Data Engineering

## Learning Goal

Build practical capability in data engineering through reusable notebooks, project READMEs, and portfolio-grade implementations.

Data Engineering is the discipline of making data trustworthy, available, and
reusable. The data engineer asks: where did this data come from, what contract
does it satisfy, what transformations produced it, and can the workflow be
rerun safely?

## Role Mental Model

```mermaid
flowchart LR
    source["Source"] --> ingest["Ingest"]
    ingest --> contract["Schema contract"]
    contract --> quality["Quality checks"]
    quality --> transform["Transform"]
    transform --> publish["Publish"]
    publish --> observe["Observe and backfill"]
```

## Core Competencies

- Define schemas, keys, units, freshness expectations, and quality checks.
- Separate raw, interim, processed, and sample data.
- Build deterministic transformations.
- Reason about idempotence, backfills, partitions, and lineage.
- Explain when local pandas workflows stop scaling and what changes next.
- Design pipeline stages as a DAG with observable checkpoints.

## Prerequisites

- Python fundamentals.
- Basic command-line usage.
- Ability to run `uv sync` and notebooks from the repository root.

## Recommended Module Order

- `00_foundations` - Foundations
- `01_python_data_stack` - Python Data Stack
- `05_data_pipelines` - Data Pipelines
- `06_big_data_and_cloud` - Big Data And Cloud Patterns
- `09_capstone_systems` - Capstone Systems

## Checkpoints

1. Write a schema for a project dataset before transformation.
2. Add row-count, null-rate, uniqueness, and valid-range checks.
3. Draw the pipeline DAG and identify rerunnable stages.
4. Explain the partitioning strategy for a larger version of the dataset.
5. Document lineage from source to report or model artifact.

## Exit Standard

A learner completes this track when they can turn a messy source table or log
stream into a documented, validated, reproducible dataset that another project
can consume without guessing column meanings or transformation history.

## Representative Projects

- `p013` [Data Assimilation for Environmental Systems](../../../projects/data_assimilation_for_environmental_systems/README.md) - `advanced`, `capstone_project`
- `p020` [Environmental Sensor Network Placement Optimizer](../../../projects/environmental_sensor_network_placement_optimizer/README.md) - `advanced`, `capstone_project`
- `p039` [Large-Scale Astronomy Catalog Linker](../../../projects/large_scale_astronomy_catalog_linker/README.md) - `advanced`, `data_engineering_project`
- `p040` [Large-Scale Log Compression and Analytics](../../../projects/large_scale_log_compression_and_analytics/README.md) - `advanced`, `data_engineering_project`
- `p043` [Large-Scale Text Mining of Scientific Literature](../../../projects/large_scale_text_mining_of_scientific_literature/README.md) - `advanced`, `data_engineering_project`
- `p049` [Network Traffic Anomaly Detection](../../../projects/network_traffic_anomaly_detection/README.md) - `advanced`, `data_engineering_project`
- `p071` [Renewable Energy Mix Optimizer](../../../projects/renewable_energy_mix_optimizer/README.md) - `advanced`, `capstone_project`
- `p076` [Scientific Data Platform for Multi-Modal Experiments](../../../projects/scientific_data_platform_for_multi_modal_experiments/README.md) - `advanced`, `data_engineering_project`
- `p077` [Scientific Experiment Metadata Knowledge Graph](../../../projects/scientific_experiment_metadata_knowledge_graph/README.md) - `advanced`, `data_engineering_project`
- `p085` [Smart City Noise Map Generator](../../../projects/smart_city_noise_map_generator/README.md) - `advanced`, `capstone_project`
- `p086` [Smart Farming Irrigation Optimizer](../../../projects/smart_farming_irrigation_optimizer/README.md) - `advanced`, `capstone_project`
- `p092` [Structural Health Monitoring Platform](../../../projects/structural_health_monitoring_platform/README.md) - `advanced`, `data_engineering_project`
- `p093` [Supply Chain as a Dynamic Network](../../../projects/supply_chain_as_a_dynamic_network/README.md) - `advanced`, `capstone_project`
- `p095` [Traffic Flow as a Physical System](../../../projects/traffic_flow_as_a_physical_system/README.md) - `advanced`, `capstone_project`
- `p097` [Warehouse Robotics Path Optimization](../../../projects/warehouse_robotics_path_optimization/README.md) - `advanced`, `capstone_project`

## Notebook Surface

Use each project README as the entry point, then open the linked notebook in `projects/<slug>/notebooks/` for guided exploration.
