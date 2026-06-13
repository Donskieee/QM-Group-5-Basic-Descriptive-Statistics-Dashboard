import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
grades = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)

fig, axes = plt.subplots(1, 1, figsize=(8, 5))

mean_grade = np.mean(grades)
median_grade = np.median(grades)

# Histogram with Mean and Median lines
# Don't forget to change "axes" to "axes[0]" once assembling it
axes.hist(grades, bins=20, color="steelblue", edgecolor="white", alpha=0.7)
axes.axvline(mean_grade, color="red", linestyle="--", linewidth=2,
                label=f"Mean = {mean_grade:.1f}")
axes.axvline(median_grade, color="green", linestyle=":", linewidth=2,
                label=f"Median = {median_grade:.1f}")

# Labels and design
axes.set_xlabel("Grade (0-100)", fontsize=11)
axes.set_ylabel("Number of Students (Frequency)", fontsize=11)
axes.set_title("Grade Distribution with Mean, Median, & Mode", fontsize=12, fontweight='bold')
axes.legend(loc="upper right", fontsize=10)
axes.grid(True, alpha=0.3, linestyle='--')

# Text annotation explaining the lines
axes.text(0.02, 0.95, f"Total Students: {len(grades)}",
             transform=axes.transAxes, fontsize=9, verticalalignment='top')

plt.tight_layout()
plt.show()
