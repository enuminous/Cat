import numpy as np
import pandas as pd

EPS = 1e-8

def robust_z(s, window=23):
    s = s.astype(float)
    med = s.rolling(window, min_periods=3).median()
    mad = (s-med).abs().rolling(window, min_periods=3).median()
    return ((s-med)/(1.4826*mad+EPS)).replace([np.inf,-np.inf], np.nan).fillna(0.0)

def build_feature_families(df, feature_columns, horizons=(3,7,23)):
    x = df[feature_columns].astype(float).copy()
    fam = {}

    local = pd.DataFrame(index=df.index)
    deriv = pd.DataFrame(index=df.index)
    rel = pd.DataFrame(index=df.index)
    contradiction = pd.DataFrame(index=df.index)
    coherence = pd.DataFrame(index=df.index)
    memory = pd.DataFrame(index=df.index)
    recursion = pd.DataFrame(index=df.index)
    interaction = pd.DataFrame(index=df.index)

    for c in feature_columns:
        local[f"{c}__x"] = x[c]
        deriv[f"{c}__dx"] = x[c].diff().fillna(0.0)
        deriv[f"{c}__ddx"] = x[c].diff().diff().fillna(0.0)

    contradiction_cols = []
    for i,a in enumerate(feature_columns):
        for b in feature_columns[i+1:]:
            d = x[a] - x[b]
            rname = f"rel__{a}__{b}"
            rel[rname] = d

            expected = d.rolling(max(horizons), min_periods=3).median()
            resid = d - expected
            mad = resid.abs().rolling(max(horizons), min_periods=3).median()
            cname = f"contradiction__{a}__{b}"
            contradiction[cname] = (resid.abs()/(1.4826*mad+EPS)).replace([np.inf,-np.inf], np.nan).fillna(0.0)
            contradiction_cols.append(cname)

    if contradiction_cols:
        coherence["coherence"] = np.exp(-contradiction[contradiction_cols]).mean(axis=1)
    else:
        coherence["coherence"] = 1.0
    coherence["coherence_velocity"] = coherence["coherence"].diff().fillna(0.0)
    coherence["coherence_acceleration"] = coherence["coherence_velocity"].diff().fillna(0.0)

    base_for_memory = pd.concat([local, deriv, rel, contradiction, coherence], axis=1).fillna(0.0)
    for h in horizons:
        memory[f"state_mean_{h}"] = base_for_memory.abs().mean(axis=1).rolling(h, min_periods=1).mean()
        memory[f"state_var_{h}"] = base_for_memory.var(axis=1).rolling(h, min_periods=1).mean().fillna(0.0)

    state = pd.concat([
        coherence["coherence"],
        coherence["coherence_velocity"],
        coherence["coherence_acceleration"],
        memory.mean(axis=1)
    ], axis=1).to_numpy()

    rec = np.zeros_like(state)
    for t in range(len(state)):
        prev = rec[t-1] if t > 0 else np.zeros(state.shape[1])
        s = state[t].copy()
        for _ in range(3):
            s = 0.5*s + 0.5*np.tanh(s + prev)
        rec[t] = s

    for j in range(rec.shape[1]):
        recursion[f"recursive_{j}"] = rec[:,j]

    if len(feature_columns) >= 2:
        for i,a in enumerate(feature_columns):
            for b in feature_columns[i+1:]:
                interaction[f"interaction__{a}__{b}"] = x[a]*x[b]

    fam["local"] = local
    fam["derivatives"] = deriv
    fam["relations"] = rel
    fam["contradiction"] = contradiction
    fam["coherence"] = coherence
    fam["memory"] = memory
    fam["recursion"] = recursion
    fam["interactions"] = interaction

    for k,v in fam.items():
        fam[k] = v.replace([np.inf,-np.inf], np.nan).fillna(0.0)

    return fam

def combine_families(families, include=None):
    keys = list(families.keys()) if include is None else list(include)
    frames = [families[k] for k in keys if k in families and families[k].shape[1] > 0]
    if not frames:
        return pd.DataFrame(index=next(iter(families.values())).index)
    return pd.concat(frames, axis=1).fillna(0.0)
