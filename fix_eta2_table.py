# fix_eta2_table.py (v2)
import json, glob, os

search_dirs = [".", ".."]
files = {}
for d in search_dirs:
    for f in glob.glob(os.path.join(d, "expert_specialization_*.json")):
        name = os.path.basename(f)
        if "SUMMARY" in name:
            continue
        # prefer the one already in current dir if duplicate; else take parent copy
        if name not in files:
            files[name] = f

rows = []
for name, path in sorted(files.items()):
    dataset = name.replace("expert_specialization_", "").replace(".json", "")
    with open(path) as fh:
        data = json.load(fh)
    stats = data.get("stats", {})
    logp = stats.get("LogP", {}).get("eta2")
    arr  = stats.get("ArRings", {}).get("eta2")
    rows.append((dataset, logp, arr, path))

print(f"{'Dataset':<30} {'LogP eta2':>12} {'ArRings eta2':>14}   Source")
print("-" * 80)
logp_vals, arr_vals = [], []
for dataset, logp, arr, path in rows:
    logp_s = f"{logp:.4f}" if logp is not None else "MISSING"
    arr_s  = f"{arr:.4f}" if arr is not None else "MISSING"
    print(f"{dataset:<30} {logp_s:>12} {arr_s:>14}   {path}")
    if logp is not None: logp_vals.append(logp)
    if arr is not None: arr_vals.append(arr)

print("-" * 80)
print(f"{'MEAN (n='+str(len(logp_vals))+')':<30} {sum(logp_vals)/len(logp_vals):>12.4f} {sum(arr_vals)/len(arr_vals):>14.4f}")

ld50_logp = next((r[1] for r in rows if "ld50" in r[0].lower()), None)
print(f"\nLD50 LogP eta2 found: {ld50_logp}")
print(f"Total datasets found: {len(rows)}  (expected ~21-22 to match TDC coverage)")

with open("eta2_corrected_summary.json", "w") as out:
    json.dump({"per_dataset": [{"dataset": d, "LogP_eta2": l, "ArRings_eta2": a, "source": p} for d,l,a,p in rows],
               "mean_LogP_eta2": sum(logp_vals)/len(logp_vals),
               "mean_ArRings_eta2": sum(arr_vals)/len(arr_vals),
               "n_datasets": len(logp_vals)}, out, indent=2)
print("\nSaved -> eta2_corrected_summary.json")