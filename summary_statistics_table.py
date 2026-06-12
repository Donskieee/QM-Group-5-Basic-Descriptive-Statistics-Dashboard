import numpy as np
import pandas as pd
from scipy import stats

# Generate synthetic student grades
np.random.seed(42)
grades = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)

# Summary Statistics Table
summary_table = pd.DataFrame({
    "Statistic": ["Min", "Max", "Mean", "Median", "Std", "Skew"],
    "Value": [
        np.min(grades),
        np.max(grades),
        np.mean(grades),
        np.median(grades),
        np.std(grades),
        stats.skew(grades)
    ]
})

print("Summary Statistics Table")
print(summary_table.round(2))
