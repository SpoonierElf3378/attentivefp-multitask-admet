# MoE-ADMET

Code and results for **"Sparse mixture-of-experts routing recovers, rather than creates, physicochemical organization of chemical space for molecular property prediction."**

An architecture-agnostic sparse top-K mixture-of-experts (MoE) plug-in for graph neural network ADMET property prediction, benchmarked across 10 MoleculeNet datasets and the 22-dataset TDC ADMET suite.

## Key findings

- **Predictive accuracy:** the MoE plug-in improves regression accuracy over a plain GCN backbone on 10/12 datasets (Wilcoxon *P* = 0.017, dataset-level), but a **parameter-matched dense ablation shows no significant advantage over routing** — comparable capacity without a router matches it.
- **Interpretability:** expert assignment aligns with physicochemical descriptors (aromatic-ring count, LogP) never shown to the router, replicating across 3 of 4 datasets. However, **k-means clustering of the same representation recovers this organization at least as strongly** (15/16 comparisons) — the chemical structure lives in the backbone's representation, not uniquely in the routing mechanism.
- Both null-control results are reported directly rather than omitted; see the manuscript's Discussion for the full reframing.

## Repository structure

```
├── results_moegcn_regr.json          # MoE-GCN, per-dataset HPO-tuned, MoleculeNet regression
├── results_moegcn_tdc_v2.json        # MoE-GCN, per-dataset HPO-tuned, TDC (tuned; use this, not results_tdc.json)
├── results_gcn_tdc.json              # Plain GCN baseline, TDC
├── ablation_routing_results.json     # Parameter-matched ablation (MoE-GCN / Dense-uniform / Dense-wide)
├── ablation_optuna_results.json      # Fixed-architecture ablation, HPO reference
├── expert_specialization_*.json      # Per-dataset η²/MI physicochemical specialization analysis
├── expert_specialization_SUMMARY.json # Consolidated η²/MI/p-values, all 4 datasets, all 8 descriptors
├── build_tdc_table_corrected.py      # Rebuilds the 22-dataset TDC table from the correct tuned source
├── reconcile_table1_table6.py        # Diagnostic: reconciles Table 1 vs Table 6 MoE-GCN provenance
├── dump_config.py                    # Diagnostic: dumps result-file config/metadata for provenance checks
├── verify_dmpnn_implementation.py    # Checks whether the DMPNN backbone implements reverse-bond exclusion
├── quantify_chemical_diversity.py    # Bemis–Murcko scaffold ratio + ECFP4 diversity, all 4 spec. datasets
├── fix_table7_seed_matching.py       # Recomputes matched-seed (n=3) MoE-GCN vs GCN comparison
├── grover/                           # GROVER submodule (see note below)
└── attentivefp-multitask-admet/      # Corrected results subfolder (canonical for a few duplicated files)
```

## Reproducing the main results

```bash
conda env create -f environment.yml   # or: conda activate moe_admet if already set up
python build_tdc_table_corrected.py   # 22-dataset TDC table
python quantify_chemical_diversity.py # chemical diversity metrics (Table S2)
```

Full training/HPO scripts and Optuna search logs for every table and figure are included; see the manuscript's Methods for the exact protocol (Bemis–Murcko scaffold splits, Optuna TPE, 5 seeds MoleculeNet / 3 seeds TDC).

## Notes on provenance

A few result files exist in two places (project root and `attentivefp-multitask-admet/`); where they differ, **the subfolder copy is canonical** (confirmed via file timestamps — the root copy is a pre-correction leftover). `results_tdc.json` at the project root is a stale, untuned run; **use `results_moegcn_tdc_v2.json`** for anything TDC-related.

GROVER baseline values in the manuscript are taken from the original published paper (Rong et al., NeurIPS 2020, GROVER-large configuration), not independently reproduced here — no complete GROVER run exists in this repository.

## Citation

If you use this code, please cite the manuscript (details and DOI in the paper's Declarations section) and the archived release on Zenodo: [DOI: 10.5281/zenodo.22157849](https://doi.org/10.5281/zenodo.22157849) *(update to the latest version DOI after the current release)*.

## License

MIT.
