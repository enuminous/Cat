from dataclasses import dataclass
import pandas as pd

from features import build_feature_families, combine_families
from ablation import all_ablations
from baselines import ProbModel
from metrics import binary_metrics

@dataclass
class CATExperiment:
    time_column: str
    target_column: str
    feature_columns: list
    horizons: tuple = (3,7,23)
    train_fraction: float = 0.65
    random_state: int = 23

    def run(self, df):
        df = df.sort_values(self.time_column).reset_index(drop=True).copy()
        cut = max(20, int(len(df)*self.train_fraction))
        y = df[self.target_column].astype(int).to_numpy()

        families = build_feature_families(df, self.feature_columns, self.horizons)
        definitions = all_ablations(list(families.keys()))

        results = {}
        for name, include in definitions.items():
            X = combine_families(families, include)
            model = ProbModel(self.random_state).fit(X.iloc[:cut], y[:cut])
            p = model.predict_proba(X.iloc[cut:])
            results[name] = {
                "families": include,
                "n_features": int(X.shape[1]),
                "metrics": binary_metrics(y[cut:], p)
            }

        full_brier = results["full"]["metrics"]["brier"]
        ranking = []

        for name, result in results.items():
            if name == "full":
                continue
            penalty = result["metrics"]["brier"] - full_brier
            ranking.append({
                "ablation": name,
                "brier": result["metrics"]["brier"],
                "ablation_penalty": float(penalty),
                "interpretation": (
                    "removal_hurt" if penalty > 0
                    else "removal_helped" if penalty < 0
                    else "no_change"
                )
            })

        ranking.sort(key=lambda x: x["ablation_penalty"], reverse=True)

        return {
            "n_total": len(df),
            "train_n": cut,
            "test_n": len(df)-cut,
            "full_metrics": results["full"]["metrics"],
            "results": results,
            "ablation_ranking": ranking,
            "interpretation": (
                "Positive ablation penalty means removing that family worsened Brier score. "
                "Negative means the removed family was harmful in this test."
            )
        }
