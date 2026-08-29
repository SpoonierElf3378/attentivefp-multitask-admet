"""
Quantify chemical diversity for the 4 expert-specialization datasets, to turn
the "AstraZeneca Lipophilicity has narrower diversity" claim into measured
data rather than an inferred narrative (review round 3, item 3).

Computes: Bemis-Murcko scaffold count / scaffold-to-molecule ratio, and
mean pairwise ECFP4 Tanimoto distance (internal diversity) on a sample.

Run from D:\\molprop_project\\ with moe_admet activated (needs rdkit).
You'll need each dataset's SMILES list -- point INPUT_FILES at wherever
you have them (likely the same source used for expert_specialization_*.json).
"""
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit import DataStructs
import random

random.seed(0)

INPUT_FILES = {
    "solubility_aqsoldb": r"D:\molprop_project\tdc_data\admet_group\solubility_aqsoldb",
    "caco2_wang": r"D:\molprop_project\tdc_data\admet_group\caco2_wang",
    "ld50_zhu": r"D:\molprop_project\tdc_data\admet_group\ld50_zhu",
    "lipophilicity_astrazeneca": r"D:\molprop_project\tdc_data\admet_group\lipophilicity_astrazeneca",
}
SMILES_COL = "Drug"
SAMPLE_SIZE = 1000  # for pairwise Tanimoto (full pairwise is O(n^2), sample for large sets)

def bemis_murcko_scaffold(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    try:
        scaffold = MurckoScaffold.GetScaffoldForMol(mol)
        return Chem.MolToSmiles(scaffold)
    except Exception:
        return None

def ecfp4(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)

def mean_pairwise_tanimoto_distance(fps):
    n = len(fps)
    if n < 2:
        return np.nan
    dists = []
    for i in range(n):
        sims = DataStructs.BulkTanimotoSimilarity(fps[i], fps[i+1:])
        dists.extend([1 - s for s in sims])
    return np.mean(dists) if dists else np.nan

results = {}
for name, folder in INPUT_FILES.items():
    try:
        df_train = pd.read_csv(f"{folder}\\train_val.csv")
        df_test = pd.read_csv(f"{folder}\\test.csv")
        df = pd.concat([df_train, df_test], ignore_index=True)
    except FileNotFoundError:
        print(f"[skip] {name}: not found at {folder} -- edit INPUT_FILES")
        continue

    smiles_list = df[SMILES_COL].dropna().tolist()
    n_mol = len(smiles_list)

    scaffolds = [bemis_murcko_scaffold(s) for s in smiles_list]
    scaffolds = [s for s in scaffolds if s is not None]
    n_scaffolds = len(set(scaffolds))
    scaffold_ratio = n_scaffolds / len(scaffolds) if scaffolds else np.nan

    sample = random.sample(smiles_list, min(SAMPLE_SIZE, n_mol))
    fps = [ecfp4(s) for s in sample]
    fps = [f for f in fps if f is not None]
    diversity = mean_pairwise_tanimoto_distance(fps)

    results[name] = {
        "n_molecules": n_mol,
        "n_unique_scaffolds": n_scaffolds,
        "scaffold_to_molecule_ratio": round(scaffold_ratio, 4),
        "mean_pairwise_tanimoto_distance": round(diversity, 4),
        "sample_size_for_diversity": len(fps),
    }
    print(f"{name}: {results[name]}")

out = pd.DataFrame(results).T
out.to_csv("chemical_diversity_metrics.csv")
print("\nSaved: chemical_diversity_metrics.csv")
print("Lower scaffold_to_molecule_ratio and lower mean_pairwise_tanimoto_distance")
print("both indicate LOWER diversity. Check whether AstraZeneca Lipophilicity")
print("is genuinely the lowest on both metrics before keeping the claim in the paper.")
