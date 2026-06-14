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

    ax1.hist(grades, bins=range(40, 101, 5), color="steelblue", edgecolor="white", alpha=0.7)
    ax1.axvline(stats_values["mean"], color="red", linestyle="--", linewidth=2, label=f'Mean = {stats_values["mean"]:.1f}')
    ax1.axvline(stats_values["median"], color="green", linestyle=":", linewidth=2, label=f'Median = {stats_values["median"]:.1f}')
    ax1.set_xlabel("Grade", fontsize=11)
    ax1.set_ylabel("Number of Students (Frequency)", fontsize=11)
    ax1.set_title("Grade Distribution with Mean, & Median", fontsize=12, fontweight='bold')
    ax1.legend(loc="upper right", fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xlim(40, 100)
    ax1.text(0.02, 0.95, f"Total Students: {len(grades)}", transform=ax1.transAxes, fontsize=9, verticalalignment='top')

    ax2.boxplot(
        grades,
        vert=False,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(marker='x', markeredgecolor='black', markerfacecolor='black'),
        boxprops=dict(facecolor="steelblue", alpha=0.5),
        medianprops=dict(color="red", linewidth=2)
    )
    ax2.set_title("Box Plot of Grades")
    ax2.set_yticks([])  # Remove the "1" on the y-axis
    ax2.plot([], [], color='red', linewidth=2, label='Median')
    ax2.plot([], [], marker='x', color='black', linestyle='None', label='Mean')
    ax2.legend(loc='upper right')

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
# (Title moved to right frame)
# -----------------------------

# -----------------------------
# (Buttons moved to the left frame below)
# -----------------------------

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
# BUTTONS (LEFT SIDE)
# -----------------------------
button_frame = tk.Frame(left_frame)
button_frame.pack(fill="x", pady=(0, 10))

btn_csv = tk.Button(button_frame, text="Load CSV File", command=load_csv, width=15, font=("Arial", 11, "bold"))
btn_csv.pack(side="left", padx=(0, 10))

def generate_random_data():
    new_grades = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)
    update_dashboard(new_grades)

btn_random = tk.Button(button_frame, text="Generate Random Data", command=generate_random_data, width=20, font=("Arial", 11, "bold"))
btn_random.pack(side="left")

# -----------------------------
# PLOTS
# -----------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 7))
fig.subplots_adjust(hspace=0.4)

stats_values = compute_stats(grades)

ax1.hist(grades, bins=range(40, 101, 5), color="steelblue", edgecolor="white", alpha=0.7)
ax1.axvline(stats_values["mean"], color="red", linestyle="--", linewidth=2, label=f'Mean = {stats_values["mean"]:.1f}')
ax1.axvline(stats_values["median"], color="green", linestyle=":", linewidth=2, label=f'Median = {stats_values["median"]:.1f}')
ax1.set_xlabel("Grade", fontsize=11)
ax1.set_ylabel("Number of Students (Frequency)", fontsize=11)
ax1.set_title("Grade Distribution with Mean, & Median", fontsize=12, fontweight='bold')
ax1.legend(loc="upper right", fontsize=10)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(40, 100)
ax1.text(0.02, 0.95, f"Total Students: {len(grades)}", transform=ax1.transAxes, fontsize=9, verticalalignment='top')

ax2.boxplot(
    grades,
    vert=False,
    patch_artist=True,
    showmeans=True,
    meanprops=dict(marker='x', markeredgecolor='black', markerfacecolor='black'),
    boxprops=dict(facecolor="steelblue", alpha=0.5),
    medianprops=dict(color="red", linewidth=2)
)
ax2.set_yticks([])  # Remove the "1" on the y-axis
ax2.plot([], [], color='red', linewidth=2, label='Median')
ax2.plot([], [], marker='x', color='black', linestyle='None', label='Mean')
ax2.legend(loc='upper right')

canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)

# -----------------------------
# TITLE & TABLE
# -----------------------------
title = tk.Label(right_frame, text="Grade Statistics Dashboard",
                 font=("Arial", 20, "bold"))
title.pack(pady=(0, 15))

# Increase font size for the table
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 13, "bold"))
style.configure("Treeview", font=("Arial", 15), rowheight=30)

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
