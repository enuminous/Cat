import pandas as pd
from features import build_feature_families, combine_families
from ablation import all_ablations
from cat import CATExperiment

def test_families_and_ablations():
    df = pd.read_csv("example_data.csv")
    fam = build_feature_families(df, ["a","b","c"])
    assert "coherence" in fam
    assert "recursion" in fam
    defs = all_ablations(list(fam.keys()))
    assert "full" in defs
    assert "minus_coherence" in defs
    assert "no_efmw_derived" in defs

def test_experiment_runs():
    df = pd.read_csv("example_data.csv")
    exp = CATExperiment(
        time_column="time",
        target_column="failure",
        feature_columns=["a","b","c"],
    )
    out = exp.run(df)
    assert "ablation_ranking" in out
    assert "full_metrics" in out
    assert len(out["ablation_ranking"]) > 0
