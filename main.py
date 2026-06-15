import numpy as np
import pandas as pd
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import stats

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")
plt.style.use('seaborn-v0_8-whitegrid')

# -----------------------------
# INITIAL DATA
# -----------------------------
np.random.seed(42)
grades = np.random.normal(loc=75, scale=12, size=100).clip(0, 100)

# -----------------------------
# STAT FUNCTIONS
# -----------------------------


def compute_stats(data):
    # Calculate mode safely
    mode_result = stats.mode(data, keepdims=True)
    mode_val = mode_result.mode[0] if len(mode_result.mode) > 0 else np.nan

    return {
        "mean": np.mean(data),
        "median": np.median(data),
        "mode": mode_val,
        "variance": np.var(data),
        "std": np.std(data),
        "range": np.max(data) - np.min(data),
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

    ax1.hist(grades, bins=range(0, 101, 10), color="steelblue", edgecolor="white", alpha=0.7)
    ax1.axvline(stats_values["mean"], color="red", linestyle="--", linewidth=2, label=f'Mean = {stats_values["mean"]:.1f}')
    ax1.axvline(stats_values["median"], color="green", linestyle=":", linewidth=2, label=f'Median = {stats_values["median"]:.1f}')
    ax1.set_xlabel("Grade", fontsize=16)
    ax1.set_ylabel("Number of Students (Frequency)", fontsize=16)
    ax1.set_title("Grade Distribution with Mean, & Median", fontsize=18, fontweight='bold')
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=15)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xlim(0, 100)
    ax1.set_xticks(range(0, 101, 10))
    ax1.text(0.02, 0.95, f"Total Students: {len(grades)}", transform=ax1.transAxes, fontsize=14, verticalalignment='top')

    ax2.boxplot(
        grades,
        vert=False,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(marker='x', markeredgecolor='black', markerfacecolor='black'),
        boxprops=dict(facecolor="steelblue", alpha=0.5),
        medianprops=dict(color="red", linewidth=2)
    )
    ax2.set_title("Box Plot of Grades", fontsize=18, fontweight='bold')
    ax2.set_xlabel("Grade", fontsize=16)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_xlim(0, 100)
    ax2.set_xticks(range(0, 101, 10))
    ax2.set_yticks([])  
    ax2.plot([], [], color='red', linewidth=2, label='Median')
    ax2.plot([], [], marker='x', color='black', linestyle='None', label='Mean')
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=15)

    canvas.draw()

    # -----------------------------
    # UPDATE TABLE
    # -----------------------------
    for row in tree.get_children():
        tree.delete(row)

    stats_data = [
        ("Count", stats_values["count"]),
        ("Mean", round(stats_values["mean"], 2)),
        ("50% (Median)", round(stats_values["median"], 2)),
        ("Mode", round(stats_values["mode"], 2)),
        ("Variance", round(stats_values["variance"], 2)),
        ("Std", round(stats_values["std"], 2)),
        ("Range", round(stats_values["range"], 2)),
        ("Min", round(stats_values["min"], 2)),
        ("25% (Q1)", round(stats_values["q1"], 2)),
        ("75% (Q3)", round(stats_values["q3"], 2)),
        ("Max", round(stats_values["max"], 2)),
        ("Skewness", round(stats_values["skew"], 4)),
        ("Kurtosis", round(stats_values["kurt"], 4)),
    ]

    for i, item in enumerate(stats_data):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert("", tk.END, values=item, tags=(tag,))
        
    # Update interpretation text
    skew_text = "fairly symmetrical"
    if stats_values["skew"] > 0.5:
        skew_text = "positively skewed (right-leaning)"
    elif stats_values["skew"] < -0.5:
        skew_text = "negatively skewed (left-leaning)"

    interp = (f"Interpretation:\n"
              f"• Center: The grades cluster around a mean of {stats_values['mean']:.1f} and a median of {stats_values['median']:.1f}.\n"
              f"• Spread: Grades span a range of {stats_values['range']:.1f} points with a standard deviation of {stats_values['std']:.1f}, indicating {'high' if stats_values['std'] > 10 else 'low'} variability.\n"
              f"• Skew: With a skewness of {stats_values['skew']:.2f}, the distribution is {skew_text}.")
    lbl_interpretation.configure(text=interp)


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
root = ctk.CTk()
root.title("Grade Statistics Dashboard")
root.geometry("1200x700")
root.configure(fg_color="#F4F6F9")

# -----------------------------
# TOP BANNER
# -----------------------------
top_banner = ctk.CTkFrame(root, fg_color="#2C3E50", corner_radius=0)
top_banner.pack(fill="x", side="top")

title = ctk.CTkLabel(top_banner, text="Grade Statistics Dashboard",
                     font=("Arial", 36, "bold"), text_color="white")
title.pack(pady=20)

# -----------------------------
# MAIN GRID LAYOUT (FIXED)
# -----------------------------
main_frame = ctk.CTkFrame(root, fg_color="transparent")
main_frame.pack(fill="both", expand=True, pady=10)

main_frame.columnconfigure(0, weight=3)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)

left_frame = ctk.CTkFrame(main_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

right_frame = ctk.CTkFrame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# -----------------------------
# BUTTONS (LEFT SIDE)
# -----------------------------
button_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
button_frame.pack(fill="x", pady=10, padx=10)

btn_csv = ctk.CTkButton(button_frame, text="Load CSV File", command=load_csv, font=("Arial", 16, "bold"))
btn_csv.pack(side="left", padx=(0, 10))

def generate_random_data():
    random_student_count = np.random.randint(40, 160)  # Random amount between 40 and 160 students
    raw_grades = np.random.normal(loc=75, scale=12, size=random_student_count).clip(0, 100)
    
    df = pd.DataFrame({"Grade": raw_grades})
    new_grades = df["Grade"].values
    
    update_dashboard(new_grades)

btn_random = ctk.CTkButton(button_frame, text="Generate Random Data", command=generate_random_data, font=("Arial", 16, "bold"))
btn_random.pack(side="left")

def export_report():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
    if file_path:
        try:
            fig.savefig(file_path, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Success", "Report exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export image:\n{str(e)}")

btn_export = ctk.CTkButton(button_frame, text="Export Report", command=export_report, font=("Arial", 16, "bold"), fg_color="#27ae60", hover_color="#2ecc71")
btn_export.pack(side="left", padx=(10, 0))

# -----------------------------
# PLOTS
# -----------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 14))
fig.subplots_adjust(hspace=0.4, right=0.75)

stats_values = compute_stats(grades)

ax1.hist(grades, bins=range(40, 101, 5), color="steelblue", edgecolor="white", alpha=0.7)
ax1.axvline(stats_values["mean"], color="red", linestyle="--", linewidth=2, label=f'Mean = {stats_values["mean"]:.1f}')
ax1.axvline(stats_values["median"], color="green", linestyle=":", linewidth=2, label=f'Median = {stats_values["median"]:.1f}')
ax1.set_xlabel("Grade", fontsize=16)
ax1.set_ylabel("Number of Students (Frequency)", fontsize=16)
ax1.set_title("Grade Distribution with Mean, & Median", fontsize=18, fontweight='bold')
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=15)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(40, 100)
ax1.text(0.02, 0.95, f"Total Students: {len(grades)}", transform=ax1.transAxes, fontsize=14, verticalalignment='top')

ax2.boxplot(
    grades,
    vert=False,
    patch_artist=True,
    showmeans=True,
    meanprops=dict(marker='x', markeredgecolor='black', markerfacecolor='black'),
    boxprops=dict(facecolor="steelblue", alpha=0.5),
    medianprops=dict(color="red", linewidth=2)
)
ax2.set_title("Box Plot of Grades", fontsize=18, fontweight='bold')
ax2.set_xlabel("Grade", fontsize=16)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(40, 100)
ax2.set_yticks([])  # Remove the "1" on the y-axis
ax2.plot([], [], color='red', linewidth=2, label='Median')
ax2.plot([], [], marker='x', color='black', linestyle='None', label='Mean')
ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=15)

canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)

# -----------------------------
# TABLE
# -----------------------------
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 20, "bold"))
style.configure("Treeview", font=("Arial", 20), rowheight=30)

columns = ("Statistic", "Value")
tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
tree.tag_configure('evenrow', background='#E8EDF2')
tree.tag_configure('oddrow', background='white')

tree.heading("Statistic", text="Statistic")
tree.heading("Value", text="Value")
tree.pack(fill="both", expand=True)

# -----------------------------
# INTERPRETATION BOX
# -----------------------------
lbl_interpretation = ctk.CTkLabel(right_frame, text="", font=("Arial", 14), justify="left", wraplength=450, anchor="w")
lbl_interpretation.pack(fill="x", pady=10, padx=10)

update_dashboard(grades)

# -----------------------------
# RUN APP
# -----------------------------
root.mainloop()
