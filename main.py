import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats

# -----------------------------
# INITIAL DATA
# -----------------------------
np.random.seed(42)
grades = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)

# -----------------------------
# STAT FUNCTIONS
# -----------------------------


def compute_stats(data):
    return {
        "mean": np.mean(data),
        "median": np.median(data),
        "std": np.std(data),
        "min": np.min(data),
        "max": np.max(data),
        "q1": np.percentile(data, 25),
        "q2": np.percentile(data, 50),
        "q3": np.percentile(data, 75),
        "skew": stats.skew(data),
        "kurt": stats.kurtosis(data),
        "count": len(data)
    }


def update_dashboard(new_grades):
    global grades, stats_values

    grades = new_grades
    stats_values = compute_stats(grades)

    # -----------------------------
    # UPDATE PLOTS
    # -----------------------------
    ax1.clear()
    ax2.clear()

    ax1.hist(grades, bins=20, color="steelblue", edgecolor="white", alpha=0.7)
    ax1.axvline(stats_values["mean"], color="red", linestyle="--", linewidth=2)
    ax1.axvline(stats_values["median"], color="green", linestyle=":")
    ax1.set_title("Grade Distribution (Histogram)")
    ax1.set_ylabel("Frequency")
    ax1.grid(alpha=0.3)

    ax2.boxplot(
        grades,
        vert=False,
        patch_artist=True,
        boxprops=dict(facecolor="steelblue", alpha=0.5),
        medianprops=dict(color="red", linewidth=2)
    )
    ax2.set_title("Box Plot of Grades")

    canvas.draw()

    # -----------------------------
    # UPDATE TABLE
    # -----------------------------
    for row in tree.get_children():
        tree.delete(row)

    stats_data = [
        ("Count", stats_values["count"]),
        ("Mean", round(stats_values["mean"], 2)),
        ("Std", round(stats_values["std"], 2)),
        ("Min", round(stats_values["min"], 2)),
        ("25%", round(stats_values["q1"], 2)),
        ("50%", round(stats_values["q2"], 2)),
        ("75%", round(stats_values["q3"], 2)),
        ("Max", round(stats_values["max"], 2)),
        ("Skewness", round(stats_values["skew"], 4)),
        ("Kurtosis", round(stats_values["kurt"], 4)),
    ]

    for item in stats_data:
        tree.insert("", tk.END, values=item)


def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if not file_path:
        return

    try:
        data = pd.read_csv(file_path)

        if "Grade" not in data.columns:
            messagebox.showerror("Error", "CSV must contain a 'Grade' column.")
            return

        new_grades = data["Grade"].dropna().values

        if len(new_grades) == 0:
            messagebox.showerror("Error", "No valid grade data found!")
            return

        update_dashboard(new_grades)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -----------------------------
# MAIN WINDOW
# -----------------------------
root = tk.Tk()
root.title("Grade Statistics Dashboard")
root.geometry("1200x700")

# -----------------------------
# TITLE
# -----------------------------
title = tk.Label(root, text="Grade Statistics Dashboard",
                 font=("Arial", 16, "bold"))
title.pack(pady=10)

# -----------------------------
# BUTTON
# -----------------------------
btn = tk.Button(root, text="Load CSV File", command=load_csv)
btn.pack(pady=5)

# -----------------------------
# MAIN GRID LAYOUT (FIXED)
# -----------------------------
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

main_frame.columnconfigure(0, weight=3)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)

left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# -----------------------------
# PLOTS
# -----------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 7))
fig.subplots_adjust(hspace=0.4)

stats_values = compute_stats(grades)

ax1.hist(grades, bins=20, color="steelblue", edgecolor="white", alpha=0.7)
ax1.axvline(stats_values["mean"], color="red", linestyle="--")
ax1.axvline(stats_values["median"], color="green", linestyle=":")
ax1.set_title("Grade Distribution (Histogram)")
ax1.grid(alpha=0.3)

ax2.boxplot(
    grades,
    vert=False,
    patch_artist=True,
    boxprops=dict(facecolor="steelblue", alpha=0.5),
    medianprops=dict(color="red", linewidth=2)
)

canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)

# -----------------------------
# TABLE
# -----------------------------
columns = ("Statistic", "Value")
tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)

tree.heading("Statistic", text="Statistic")
tree.heading("Value", text="Value")
tree.pack(fill="both", expand=True)

update_dashboard(grades)

# -----------------------------
# RUN APP
# -----------------------------
root.mainloop()
