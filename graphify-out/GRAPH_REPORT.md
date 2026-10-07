# Graph Report - Workspace  (2026-10-07)

## Corpus Check
- 38 files · ~911,388 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 35 file(s) not represented in the graph (top: .csv 31, (none) 3, .code-workspace 1)

## Summary
- 210 nodes · 609 edges · 28 communities (10 shown, 18 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `590a89df`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- pandas
- os
- config.py
- expl_utils.py
- run_pipeline.py
- load_industry_data
- get_industry_names
- get_models
- expl_jointwald.py
- Cross-Sectoral Sensitivities of Asset Pricing Models
- asset-pricing-sector-sensitivities
- expl_tables.py
- ponytail.md

## God Nodes (most connected - your core abstractions)
1. `main()` - 20 edges
2. `load_industry_data()` - 18 edges
3. `get_industry_names()` - 18 edges
4. `load_factors()` - 17 edges
5. `set_academic_style()` - 17 edges
6. `get_models()` - 15 edges
7. `main()` - 14 edges
8. `main()` - 14 edges
9. `load_data_with_markers()` - 13 edges
10. `process_model_statistics()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `run_data_stage()` --calls--> `process_data()`  [EXTRACTED]
  run_pipeline.py → src/data/data_processing.py
- `run_in_sample_stage()` --calls--> `main()`  [EXTRACTED]
  run_pipeline.py → src/modeling/in_sample/expl_assumptions.py
- `run_in_sample_stage()` --calls--> `main()`  [EXTRACTED]
  run_pipeline.py → src/modeling/in_sample/expl_bydecs.py
- `run_in_sample_stage()` --calls--> `run_all_analyses()`  [EXTRACTED]
  run_pipeline.py → src/modeling/in_sample/expl_descript.py
- `run_in_sample_stage()` --calls--> `main()`  [EXTRACTED]
  run_pipeline.py → src/modeling/in_sample/expl_incrwald.py

## Import Cycles
- None detected.

## Communities (28 total, 18 thin omitted)

### Community 0 - "pandas"
Cohesion: 0.13
Nodes (11): get_standard_datasets(), process_data(), export_processing_statistics(), load_data_with_markers(), save_with_markers(), main(), test_models_and_export(), test_date_alignment_across_processed_datasets() (+3 more)

### Community 1 - "os"
Cohesion: 0.23
Nodes (18): run_all_analyses(), plot_cumulative_log_factor_returns(), plot_cumulative_log_industry_returns(), plot_decade_model_alpha_grids(), plot_decade_model_factor_grids(), plot_decade_rsquared_grid(), plot_factor_distributions(), plot_industry_distributions() (+10 more)

### Community 2 - "config.py"
Cohesion: 0.24
Nodes (6): get_coeffsbydecs_path(), get_comp_path(), get_descript_model_path(), get_params_path(), get_resids_path(), get_statssum_path()

### Community 3 - "expl_utils.py"
Cohesion: 0.15
Nodes (12): main(), write_model_statistics(), collect_industry_statistics(), get_regression_parameters(), process_model_statistics(), run_regression_analysis(), save_regression_summary(), test_homoskedasticity() (+4 more)

### Community 4 - "run_pipeline.py"
Cohesion: 0.11
Nodes (14): main(), run_data_stage(), run_in_sample_stage(), run_out_of_sample_stage(), extract_market_factor_data(), run_analysis(), calculate_paired_t_test(), main() (+6 more)

### Community 5 - "load_industry_data"
Cohesion: 0.27
Nodes (8): calculate_and_save_descriptive_stats(), write_descriptive_stats_industry(), write_descriptive_stats_model(), calculate_descriptive_stats(), load_data(), load_factors(), load_industry_data(), sample_factor_and_excess_industry_data()

### Community 6 - "get_industry_names"
Cohesion: 0.67
Nodes (6): main(), write_incrwald_results(), calculate_excess_returns(), get_industry_names(), perform_hac_wald_test(), run_all_regressions()

### Community 7 - "get_models"
Cohesion: 0.67
Nodes (5): main(), filter_data_by_period(), get_decades(), get_models(), run_regression_by_decade()

### Community 8 - "expl_jointwald.py"
Cohesion: 0.18
Nodes (8): main(), perform_joint_wald_test(), write_jointwald_results(), add_average_row(), run_regression(), test_joint_wald_test(), test_model_configurations(), test_ols_regression_with_hac()

### Community 9 - "Cross-Sectoral Sensitivities of Asset Pricing Models"
Cohesion: 0.11
Nodes (18): 1. Environment Setup, 2. Execute the Full Empirical Pipeline, 3. Stage-by-Stage Execution, 4. Running the Test Suite, 👤 Academic Citation & Contact, Cross-Sectoral Sensitivities of Asset Pricing Models, Cumulative Factor Dynamics (1963–2024), 📐 Econometric Methodology (+10 more)

## Knowledge Gaps
- **16 isolated node(s):** `asset-pricing-sector-sensitivities`, `Ponytail, lazy senior dev mode`, `Empirical Evaluation of CAPM, Fama-French 3-Factor, and 5-Factor Models Across Industry Portfolios (1963–2024)`, `📌 Executive Summary & Abstract`, `🔍 Key Empirical Findings` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 74 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `expl_utils.py` to `pandas`, `os`, `config.py`, `run_pipeline.py`, `load_industry_data`, `get_industry_names`, `get_models`, `expl_jointwald.py`, `expl_tables.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `get_industry_names()` (e.g. with `test_models_and_export()` and `train_models_and_export()`) actually correct?**
  _`get_industry_names()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `asset-pricing-sector-sensitivities`, `Ponytail, lazy senior dev mode`, `Empirical Evaluation of CAPM, Fama-French 3-Factor, and 5-Factor Models Across Industry Portfolios (1963–2024)` to the rest of the system?**
  _16 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `pandas` be split into smaller, more focused modules?**
  _Cohesion score 0.1339031339031339 - nodes in this community are weakly interconnected._
- **Why does `load_data_with_markers()` connect `pandas` to `os`, `run_pipeline.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `run_pipeline.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11088709677419355 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `os` to `pandas`, `run_pipeline.py`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._