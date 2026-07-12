# ML Engineering

## Learning Goal

Build practical capability in ml engineering through reusable notebooks, project READMEs, and portfolio-grade implementations.

ML Engineering is the discipline of turning modeling work into repeatable,
inspectable systems. The ML engineer asks: can this model be trained again,
evaluated consistently, served through a stable interface, monitored, and
replaced when it fails?

## Role Mental Model

```mermaid
flowchart LR
    data["Data contract"] --> train["Train"]
    train --> evaluate["Evaluate"]
    evaluate --> package["Package"]
    package --> serve["Serve"]
    serve --> monitor["Monitor"]
    monitor --> retrain["Retrain or rollback"]
```

## Core Competencies

- Separate training, evaluation, inference, and app/demo logic.
- Record parameters, metrics, artifacts, data assumptions, and code version.
- Define input and output contracts for inference.
- Monitor data drift, prediction drift, and operational errors.
- Design rollback and retraining criteria.
- Communicate model risks through model cards or README limitations.

## Prerequisites

- Python fundamentals.
- Basic command-line usage.
- Ability to run `uv sync` and notebooks from the repository root.

## Recommended Module Order

- `00_foundations` - Foundations
- `04_machine_learning` - Machine Learning
- `05_data_pipelines` - Data Pipelines
- `07_mlops_and_serving` - MLOps And Serving
- `09_capstone_systems` - Capstone Systems

## Checkpoints

1. Produce a reproducible training command and evaluation output.
2. Define the prediction input schema and error behavior.
3. Save or document artifacts and metrics for comparison.
4. Explain monitoring signals for drift and model decay.
5. Write a model limitation and rollback policy.

## Exit Standard

A learner completes this track when they can convert a project model into a
repeatable training and inference workflow with documented contracts,
evaluation gates, and operational limits.

## Representative Projects

- `p013` [Data Assimilation for Environmental Systems](../../../projects/data_assimilation_for_environmental_systems/README.md) - `advanced`, `capstone_project`
- `p020` [Environmental Sensor Network Placement Optimizer](../../../projects/environmental_sensor_network_placement_optimizer/README.md) - `advanced`, `capstone_project`
- `p034` [Human Activity Recognition from Wearables](../../../projects/human_activity_recognition_from_wearables/README.md) - `advanced`, `ml_engineering_project`
- `p039` [Large-Scale Astronomy Catalog Linker](../../../projects/large_scale_astronomy_catalog_linker/README.md) - `advanced`, `data_engineering_project`
- `p040` [Large-Scale Log Compression and Analytics](../../../projects/large_scale_log_compression_and_analytics/README.md) - `advanced`, `data_engineering_project`
- `p041` [Large-Scale Recommendation for Learning Paths](../../../projects/large_scale_recommendation_for_learning_paths/README.md) - `advanced`, `ml_engineering_project`
- `p043` [Large-Scale Text Mining of Scientific Literature](../../../projects/large_scale_text_mining_of_scientific_literature/README.md) - `advanced`, `data_engineering_project`
- `p049` [Network Traffic Anomaly Detection](../../../projects/network_traffic_anomaly_detection/README.md) - `advanced`, `data_engineering_project`
- `p067` [Real-Time Manufacturing Yield Dashboard](../../../projects/real_time_manufacturing_yield_dashboard/README.md) - `advanced`, `ml_engineering_project`
- `p068` [Recommender System for Scientific Papers](../../../projects/recommender_system_for_scientific_papers/README.md) - `advanced`, `ml_engineering_project`
- `p071` [Renewable Energy Mix Optimizer](../../../projects/renewable_energy_mix_optimizer/README.md) - `advanced`, `capstone_project`
- `p076` [Scientific Data Platform for Multi-Modal Experiments](../../../projects/scientific_data_platform_for_multi_modal_experiments/README.md) - `advanced`, `data_engineering_project`
- `p077` [Scientific Experiment Metadata Knowledge Graph](../../../projects/scientific_experiment_metadata_knowledge_graph/README.md) - `advanced`, `data_engineering_project`
- `p078` [Scientific Image Segmentation Benchmark](../../../projects/scientific_image_segmentation_benchmark/README.md) - `advanced`, `ml_engineering_project`
- `p082` [Sensor Drift Detection in Industrial Systems](../../../projects/sensor_drift_detection/README.md) - `advanced`, `ml_engineering_project`
- `p085` [Smart City Noise Map Generator](../../../projects/smart_city_noise_map_generator/README.md) - `advanced`, `capstone_project`
- `p086` [Smart Farming Irrigation Optimizer](../../../projects/smart_farming_irrigation_optimizer/README.md) - `advanced`, `capstone_project`
- `p087` [Smart Grid Fault Localization](../../../projects/smart_grid_fault_localization/README.md) - `advanced`, `ml_engineering_project`
- `p092` [Structural Health Monitoring Platform](../../../projects/structural_health_monitoring_platform/README.md) - `advanced`, `data_engineering_project`
- `p093` [Supply Chain as a Dynamic Network](../../../projects/supply_chain_as_a_dynamic_network/README.md) - `advanced`, `capstone_project`
- `p095` [Traffic Flow as a Physical System](../../../projects/traffic_flow_as_a_physical_system/README.md) - `advanced`, `capstone_project`
- `p097` [Warehouse Robotics Path Optimization](../../../projects/warehouse_robotics_path_optimization/README.md) - `advanced`, `capstone_project`
- `p100` [Wind Turbine Failure Early Warning System](../../../projects/wind_turbine_failure_early_warning_system/README.md) - `advanced`, `ml_engineering_project`

## Notebook Surface

Use each project README as the entry point, then open the linked notebook in `projects/<slug>/notebooks/` for guided exploration.
