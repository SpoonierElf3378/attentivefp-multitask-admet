"""
PyTDC caches downloaded data in its own format/location, not plain CSVs named
after the dataset. Find the actual cache and check what format it's in.
Run from D:\\molprop_project\\ with moe_admet activated.
"""
import os
import glob

print("Checking tdc_data/ directory contents:\n")
if os.path.isdir("tdc_data"):
    for root, dirs, files in os.walk("tdc_data"):
        for f in files:
            full = os.path.join(root, f)
            print(f"  {full}  ({os.path.getsize(full):,} bytes)")
else:
    print("  tdc_data/ does not exist at project root")

print("\nSearching whole project for any file with these dataset names (any extension):\n")
targets = ["caco2_wang", "ld50_zhu", "solubility_aqsoldb", "lipophilicity_astrazeneca",
           "Caco2_Wang", "LD50_Zhu", "Solubility_AqSolDB", "Lipophilicity_AstraZeneca"]
for t in targets:
    hits = glob.glob(f"**/*{t}*", recursive=True)
    print(f"[{t}]")
    for h in hits[:10]:
        print(f"  {h}")
    if not hits:
        print("  (no matches)")
    print()

print("Also trying a direct PyTDC load to see where it actually caches data:")
try:
    from tdc.single_pred import ADME
    data = ADME(name='Caco2_Wang')
    df = data.get_data()
    print(f"\nLoaded Caco2_Wang via PyTDC directly: {len(df)} rows")
    print(df.head(2))
    print("\nCheck for a 'data/' folder that just got created/used near your working directory.")
except Exception as e:
    print(f"PyTDC direct load failed: {e}")
