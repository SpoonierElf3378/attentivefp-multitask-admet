"""
Find where the actual SMILES data for the 4 expert-specialization datasets
lives, since quantify_chemical_diversity.py's guessed paths didn't exist.
Run from D:\\molprop_project\\ with moe_admet activated.
"""
import glob
import os

targets = ["solubility_aqsoldb", "caco2_wang", "ld50_zhu", "lipophilicity_astrazeneca",
           "aqsoldb", "caco2", "ld50", "lipophilicity", "lipo"]

print("Searching for CSV files matching dataset names...\n")
all_csvs = glob.glob("**/*.csv", recursive=True)
print(f"Found {len(all_csvs)} total CSV files in project.\n")

matches = {}
for csv in all_csvs:
    name_lower = os.path.basename(csv).lower()
    for t in targets:
        if t in name_lower:
            matches.setdefault(t, []).append(csv)

for t, files in matches.items():
    print(f"[{t}]")
    for f in files:
        size = os.path.getsize(f)
        print(f"  {f}  ({size:,} bytes)")
    print()

if not matches:
    print("No obvious matches by filename. Check tdc_data/ and data/ folders directly:")
    for d in ["tdc_data", "data"]:
        if os.path.isdir(d):
            print(f"\n{d}/ contents:")
            for f in os.listdir(d):
                print(" ", f)
