import numpy as np
import matplotlib.pyplot as plt


class BoxPlot:
    # Generates a box plot with quartile, outlier, and spread info.

    def __init__(self, data, label="Grades"):
        # Store the data and label
        self.data = np.array(data)
        self.label = label
        # Compute stats on init
        self._compute_stats()

    def _compute_stats(self):
        # Calculate quartiles, IQR, bounds, and outliers.
        self.q1 = np.percentile(self.data, 25)
        self.median = np.percentile(self.data, 50)
        self.q3 = np.percentile(self.data, 75)
        self.iqr = self.q3 - self.q1
        # Whisker bounds for outlier detection
        self.lower_bound = self.q1 - 1.5 * self.iqr
        self.upper_bound = self.q3 + 1.5 * self.iqr
        # Points outside the whisker bounds
        self.outliers = self.data[
            (self.data < self.lower_bound) | (self.data > self.upper_bound)
        ]

    def print_summary(self):
        # Print quartile and spread info to the console.
        print(f"Q1 (25th)     : {self.q1:.2f}")
        print(f"Median (50th) : {self.median:.2f}")
        print(f"Q3 (75th)     : {self.q3:.2f}")
        print(f"IQR           : {self.iqr:.2f}")
        print(f"Lower Bound   : {self.lower_bound:.2f}")
        print(f"Upper Bound   : {self.upper_bound:.2f}")
        print(f"Outliers      : {self.outliers if len(self.outliers) > 0 else 'None'}")

    def plot(self):
        # Render the box plot with quartile annotations.
        fig, ax = plt.subplots(figsize=(6, 7))

        # Draw the box plot
        bp = ax.boxplot(
            self.data,
            vert=True,
            patch_artist=True,
            boxprops=dict(facecolor="steelblue", alpha=0.5),
            medianprops=dict(color="red", linewidth=2),
            flierprops=dict(marker="o", markerfacecolor="red", markersize=6),
        )

        # Annotate Q1, Median, Q3 on the right side
        ax.annotate(f"Q1 = {self.q1:.1f}", xy=(1.15, self.q1),
                    fontsize=9, color="blue")
        ax.annotate(f"Median = {self.median:.1f}", xy=(1.15, self.median),
                    fontsize=9, color="red")
        ax.annotate(f"Q3 = {self.q3:.1f}", xy=(1.15, self.q3),
                    fontsize=9, color="blue")

        # Title and labels
        ax.set_title(f"Box Plot of {self.label}", fontsize=13, fontweight="bold")
        ax.set_ylabel(self.label)
        ax.set_xticks([])

        plt.tight_layout()
        plt.show()


#  Note: this part ay para sa testing lang, pwede iwanan o burahin basta d mag conflict sa main function
if __name__ == "__main__":
    # Generate synthetic student grades 
    np.random.seed(42)
    grades = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)

    # Create BoxPlot, print stats, and show plot
    box = BoxPlot(grades, label="Student Grades")
    box.print_summary()
    box.plot()
