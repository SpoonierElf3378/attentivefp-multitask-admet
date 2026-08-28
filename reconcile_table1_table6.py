"""
Reconcile Table 1 vs Table 6 MoE-GCN discrepancy (review items 2.1, 2.2).
Run from D:\\molprop_project\\ with moe_admet activated.

Scans every *.json under the project for MoE-GCN entries on
ESOL / FreeSolv / Lipo / Caco-2, and prints:
  - file path
  - dataset, mean, std
  - seed count (len of per-seed list if present)
  - any HPO/config metadata found alongside the result (n_trials, budget, seeds used)

Goal: find the source file for Table 6's numbers and see what config field
differs from the Table 1 source (results_moegcn_regr.json).
"""
import json
import glob
import os

TARGET_DATASETS = {"ESOL", "FreeSolv", "Lipo", "Lipophilicity", "Caco2", "Caco-2", "Caco2_Wang"}
TABLE1_VALUES = {
    "ESOL": 1.067,
    "FreeSolv": 3.591,
    "Lipo": 0.722,
}
TABLE6_VALUES = {
    "ESOL": 1.118,
    "FreeSolv": 3.067,
    "Lipo": 0.783,
    "Caco2": 0.540,
}

def walk_json(obj, path=""):
    """Yield (path, value) for every leaf dict that looks like a result entry."""
    if isinstance(obj, dict):
        keys_lower = {k.lower() for k in obj.keys()}
        if {"mean", "std"} <= keys_lower or {"rmse_mean"} <= keys_lower:
            yield path, obj
        for k, v in obj.items():
            yield from walk_json(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_json(v, f"{path}[{i}]")

def main():
    root = os.getcwd()
    json_files = glob.glob(os.path.join(root, "**", "*.json"), recursive=True)
    print(f"Scanning {len(json_files)} JSON files under {root}\n")

    hits = []
    for fp in json_files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            continue

        for path, entry in walk_json(data):
            path_str = f"{fp}::{path}".lower()
            for ds in TARGET_DATASETS:
                if ds.lower() in path_str:
                    hits.append((fp, path, ds, entry))

    if not hits:
        print("No matching entries found. Check TARGET_DATASETS / your JSON schema.")
        return

    print(f"{'File':<60} {'Path':<30} {'Dataset':<10} {'Mean':>8} {'Std':>8} {'n_seeds':>8}")
    print("-" * 130)
    for fp, path, ds, entry in hits:
        mean = entry.get("mean", entry.get("rmse_mean", "?"))
        std = entry.get("std", entry.get("rmse_std", "?"))
        seeds = entry.get("seeds", entry.get("n_seeds", entry.get("seed_results", "?")))
        n_seeds = len(seeds) if isinstance(seeds, list) else seeds
        # extra config clues if present nearby
        cfg_keys = [k for k in entry.keys() if k.lower() in
                    ("n_trials", "hpo_budget", "budget", "search_space", "config", "tag")]
        cfg_str = ", ".join(f"{k}={entry[k]}" for k in cfg_keys)
        rel = os.path.relpath(fp, root)
        print(f"{rel:<60} {path:<30} {ds:<10} {str(mean):>8} {str(std):>8} {str(n_seeds):>8}  {cfg_str}")

    print("\n--- Compare against paper values ---")
    print("Table 1:", TABLE1_VALUES)
    print("Table 6:", TABLE6_VALUES)
    print("\nFor each dataset above, match the printed mean to whichever paper table it")
    print("equals, then check that file's config/log for HPO trial count, seed list,")
    print("and search space size. That difference is your answer for 2.1.")
    print("Caco-2: same exercise, but also grep the manuscript's Results-section source")
    print("(likely a separate script/notebook) for where 0.366 was computed from.")

if __name__ == "__main__":
    main()
