"""
Dump the full top-level keys/config of the files behind the 2.1/2.2 conflict,
so we can see what differs between runs (not just the mean/std leaf values).
Run from D:\\molprop_project\\ with moe_admet activated.
"""
import json

FILES = [
    "results_moegcn_regr.json",
    "ablation_routing_results.json",
    "ablation_optuna_results.json",
    "results_moegcn_tdc_v2.json",
    "results_tdc.json",
]

def summarize(obj, prefix="", depth=0, max_depth=3):
    if depth > max_depth:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                print("  " * depth + f"{prefix}{k}:")
                summarize(v, "", depth + 1, max_depth)
            else:
                print("  " * depth + f"{prefix}{k} = {v}")
    elif isinstance(obj, list) and obj and not isinstance(obj[0], (dict, list)):
        print("  " * depth + f"{prefix}(list, len={len(obj)}) = {obj[:10]}")

for fp in FILES:
    print("=" * 80)
    print(fp)
    print("=" * 80)
    try:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("  NOT FOUND")
        continue
    if isinstance(data, dict):
        print("Top-level keys:", list(data.keys())[:20])
    summarize(data, max_depth=2)
    print()
