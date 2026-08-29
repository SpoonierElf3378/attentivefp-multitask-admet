"""
Verify whether the DMPNN implementation genuinely does directed edge-message
passing per Yang et al. (D-MPNN), or just uses NNConv+GRUCell without the two
defining properties: (1) hidden states live on directed bonds, not atoms, and
(2) a message on bond i->j never incorporates the reverse message j->i (the
"reverse-bond exclusion" that distinguishes D-MPNN from ordinary edge-conv).

Run from D:\\molprop_project\\ with moe_admet activated. Points you at the
exact lines to read by hand -- this can't be fully automated, but narrows
down what to check in dmpnn_regr_fixed.py / moedmpnn_regr_fixed.py.
"""
import glob
import re

candidates = [f for f in glob.glob("*dmpnn*.py") + glob.glob("**/*dmpnn*.py", recursive=True)
              if "fixed" in f.lower() or "regr" in f.lower() or "classif" in f.lower()]
candidates = sorted(set(candidates))

print(f"Found {len(candidates)} DMPNN implementation files:")
for c in candidates:
    print(" ", c)

print("\n" + "=" * 70)
print("Searching each for the two defining D-MPNN properties...")
print("=" * 70)

for f in candidates:
    print(f"\n--- {f} ---")
    with open(f, "r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read()

    # 1. Directed bond hidden state: look for edge_index being used to build
    #    a per-directed-edge hidden state (not just node features)
    has_edge_hidden = bool(re.search(r"edge_(hidden|state|attr).*edge_index|h_e\b|edge2edge|bond.*hidden", content, re.IGNORECASE))
    print(f"  Directed edge/bond hidden-state pattern found: {has_edge_hidden}")

    # 2. Reverse-bond exclusion: look for anything referencing reverse edges,
    #    "rev", "b2revb", or subtracting the reverse message
    has_reverse_exclusion = bool(re.search(r"rev(erse)?[\s_]*(bond|edge)|b2rev|exclude.*reverse", content, re.IGNORECASE))
    print(f"  Reverse-bond exclusion pattern found: {has_reverse_exclusion}")

    # 3. Check if it's just wrapping torch_geometric.nn.NNConv directly on
    #    node features with no separate edge-hidden-state bookkeeping
    uses_nnconv = "NNConv" in content
    print(f"  Uses torch_geometric NNConv: {uses_nnconv}")

    if uses_nnconv and not (has_edge_hidden and has_reverse_exclusion):
        print("  >>> LIKELY ISSUE: uses NNConv but no clear directed-edge-hidden-state")
        print("      or reverse-bond-exclusion logic found by this search.")
        print("      This means it may functionally be closer to a standard")
        print("      edge-conditioned GNN than a true D-MPNN. Read this file")
        print("      by hand around the message-passing loop to confirm.")

print("""
--- What to do with the result ---
If NEITHER pattern is found in any file: the manuscript's "genuine directed
edge-message passing" claim is not supported by the code as written, and the
text should be softened to something like "an edge-conditioned message-passing
network using NNConv with a GRUCell update" without claiming D-MPNN fidelity,
OR the reverse-bond exclusion should actually be implemented before submission.

If found: quote the specific function/line to me and I'll help word the
Methods claim precisely (e.g. citing exactly how reverse-bond messages are
excluded), rather than leaving the current blanket claim unverified.
""")
