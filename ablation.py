from itertools import combinations

DEFAULT_FAMILIES = [
    "local",
    "derivatives",
    "relations",
    "contradiction",
    "coherence",
    "memory",
    "recursion",
    "interactions",
]

def single_family_ablations(families=None):
    families = DEFAULT_FAMILIES if families is None else list(families)
    return {
        f"minus_{f}": [x for x in families if x != f]
        for f in families
    }

def joint_ablations(families=None):
    families = DEFAULT_FAMILIES if families is None else list(families)
    out = {}
    important_pairs = [
        ("coherence","recursion"),
        ("contradiction","coherence"),
        ("relations","contradiction"),
        ("memory","recursion"),
    ]
    for a,b in important_pairs:
        if a in families and b in families:
            out[f"minus_{a}_and_{b}"] = [x for x in families if x not in {a,b}]
    return out

def all_ablations(families=None):
    families = DEFAULT_FAMILIES if families is None else list(families)
    out = {"full": families}
    out.update(single_family_ablations(families))
    out.update(joint_ablations(families))
    # "No EFMW-derived" keeps the generic local/derivative/interaction capacity only.
    keep = [x for x in ["local","derivatives","interactions"] if x in families]
    out["no_efmw_derived"] = keep
    return out
