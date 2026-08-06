# Sparse Mixture-of-Experts Routing for Molecular Property Prediction

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21827442.svg)](https://doi.org/10.5281/zenodo.21827442)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)]()

Implementation of sparse Mixture-of-Experts (MoE) routing for graph neural networks applied to molecular property prediction.

The repository contains implementations of GCN, D-MPNN and sparse MoE variants together with benchmarking, parameter-matched ablation studies, expert-specialization analyses, and figure-generation scripts.

---

# Overview

This project investigates two independent questions:

1. Can sparse MoE routing improve molecular property prediction?

2. What chemical organization emerges when sparse routing is learned without explicit chemical supervision?

Unlike previous approaches, the router receives **no**

- molecular descriptors
- physicochemical properties
- Lipinski features
- handcrafted substructures
- expert labels

Expert assignments emerge entirely through end-to-end optimization.

The repository emphasizes **mechanistic analysis** rather than leaderboard performance.

---

# Features

- Sparse top-K Mixture-of-Experts routing
- GCN baseline
- D-MPNN backbone
- MoleculeNet benchmarks
- Therapeutics Data Commons (TDC) benchmarks
- Parameter-matched routing ablations
- Optuna hyperparameter optimization
- Statistical significance testing
- Expert-specialization analysis
- Figure generation scripts
- Complete reproducibility pipeline

---

# Repository Structure

```text
.
├── attentivefp_moe.py
├── ablation_routing.py
├── baselines/
├── configs/
├── data/
├── docs/
├── figures/
├── results/
├── scripts/
├── requirements.txt
├── environment.yml
└── LICENSE
```

---

# Installation

```bash
git clone https://github.com/Saptasamudra-Gogoi/attentivefp-multitask-admet.git

cd attentivefp-multitask-admet

conda env create -f environment.yml

conda activate moe_admet
```

or

```bash
pip install -r requirements.txt
```

---

# Running Experiments

Main benchmark

```bash
python attentivefp_moe.py
```

Parameter-matched ablation

```bash
python ablation_routing.py
```

Statistical analysis

```bash
python sig_test.py
```

---

# Datasets

Public datasets used in this repository

- MoleculeNet
- Therapeutics Data Commons (TDC)

---

# Reproducibility

The repository includes

- training code
- benchmark scripts
- raw results
- statistical analyses
- figure generation
- expert-specialization analyses

allowing every major experiment to be reproduced.

---

# Citation

If you use this repository, please cite the accompanying publication once available.

Software DOI

10.5281/zenodo.21827442

---

# License

MIT