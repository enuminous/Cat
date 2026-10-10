# CAT

<!-- ENUMINOUS-NETWORK:START -->
**eNuminous network:** [All repositories](https://enuminous.github.io/EFMW/repositories.html) · [EFMW](https://enuminous.github.io/EFMW/) · [102 equations](https://github.com/enuminous/Monolithic_102_EFMW) · [165 triplets](https://enuminous.github.io/FieldSpace/) · [Zoo](https://enuminous.github.io/Tortoise/) · [Lean](https://enuminous.github.io/Aristotle-102-Monolithic-Lean/) · [Engine](https://enuminous.github.io/Archimedes-Engine/) · [Papers](https://enuminous.github.io/medium/papers-essays-index.html) · [Audit](https://github.com/enuminous/EFMW_Post156_Zoo_Audit/blob/main/portfolio/INTERLOCK_AUDIT.md)

[Repository](https://github.com/enuminous/Cat) · This repository is linked through its source; GitHub Pages is not enabled.
<!-- ENUMINOUS-NETWORK:END -->

**Coherence Ablation Tester**

CAT is an EFMW-derived mechanism-discovery framework.

Its job is not to predict a domain directly.

Its job is:

> Take a candidate model that appears to work, remove one component at a time, and determine which operations are actually responsible for performance.

## Intended uses

- EFMW/TORTOISE mechanism discovery
- feature-family ablation
- recursive architecture testing
- observability-stack reduction
- AI reliability research
- model simplification
- causal contribution screening
- identifying redundant complexity

## Core cycle

```text
full candidate
→ freeze components
→ generate ablations
→ train/evaluate identically
→ measure performance loss
→ rank contribution
→ test interactions
→ keep only what earns its complexity
```

## Flat-stack repository

```text
README.md
LICENSE
CITATION.cff
pyproject.toml
requirements.txt
cat.py
ablation.py
features.py
baselines.py
metrics.py
freeze.py
ablation_schema.json
example_config.yaml
example_data.csv
example_run.py
test_cat.py
MANIFEST.sha256
```

## Scientific hypothesis

CAT itself has no preferred EFMW result.

Its rule is:

> A component is provisionally useful only if removing it produces a reproducible degradation in out-of-sample performance under matched conditions.

## Built-in ablation families

The example stack supports:

- local state
- temporal derivatives
- relational features
- contradiction
- coherence
- multiscale memory
- recursion proxy
- interaction terms

CAT can remove:

- one family at a time
- multiple families jointly
- all EFMW-derived families
- randomized/shuffled versions of selected families

## Primary metric

Default:

- Brier score

Contribution score:

```text
ablation_penalty = Brier(ablated) - Brier(full)
```

Positive means removing the component hurt performance.

Negative means the component was harmful.

Zero means it was unnecessary under the tested conditions.

## Important interpretation rule

A component is **not** considered causal merely because its ablation hurts performance.

Ablation establishes functional dependence within the tested model.

Stronger mechanism claims require:

- replication
- capacity matching
- alternative representations
- randomized controls
- perturbation/intervention when possible

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python example_run.py
```

## Tests

```bash
pytest -q
```

## Minimal use

```python
import pandas as pd
from cat import CATExperiment

df = pd.read_csv("example_data.csv")

exp = CATExperiment(
    time_column="time",
    target_column="failure",
    feature_columns=["a","b","c"],
    random_state=23,
)

print(exp.run(df))
```

## Freeze discipline

Before running CAT on a serious candidate, freeze:

- full candidate feature families
- ablation definitions
- data split
- seeds
- model class
- parameter budget
- metric
- exclusions
- stopping rule

Do not redefine the "important" component after seeing results.

## Negative results

If removing an EFMW component does not hurt performance, delete or demote it.

If removing it improves performance, it is actively harmful under the tested conditions.

## Status

Research software. Experimental.
