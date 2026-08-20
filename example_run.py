import json
import pandas as pd
from cat import CATExperiment

df = pd.read_csv("example_data.csv")

exp = CATExperiment(
    time_column="time",
    target_column="failure",
    feature_columns=["a","b","c"],
    horizons=(3,7,23),
    random_state=23,
)

result = exp.run(df)
print(json.dumps(result, indent=2))
