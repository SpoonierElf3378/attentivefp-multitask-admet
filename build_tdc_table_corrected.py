import json
import pandas as pd

with open("results_moegcn_tdc_v2.json") as f:
    moe = json.load(f)
with open("results_gcn_tdc.json") as f:
    gcn = json.load(f)

rows = []
for ds, e in moe.items():
    rows.append({"dataset": ds, "model": "MoE-GCN", "mean": e["mean"], "std": e["std"], "n_seeds": e.get("n_seeds", 5)})
for ds, e in gcn.items():
    if not isinstance(e, dict):
        continue
    rows.append({"dataset": ds, "model": "GCN", "mean": e.get("mean"), "std": e.get("std"), "n_seeds": e.get("n_seeds", 3)})

df = pd.DataFrame(rows)
pivot = df.pivot_table(index="dataset", columns="model", values=["mean", "std", "n_seeds"])
pivot.to_csv("tdc_full_22_dataset_table_CORRECTED.csv")
print(pivot)
print(f"\nDatasets: {df['dataset'].nunique()}")
