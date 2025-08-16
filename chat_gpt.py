import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Generate fake CSV-like data
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
sales = np.random.randint(50, 200, size=100)
profit = sales * np.random.uniform(0.1, 0.3, size=100)
customers = np.random.randint(20, 80, size=100)

df = pd.DataFrame({
    "Date": dates,
    "Sales": sales,
    "Profit": profit,
    "Customers": customers
})

# Create figure with 2x2 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 8))
fig.suptitle("Business Analytics Dashboard", fontsize=16, fontweight="bold")

# ---- 1. Time-series Line Chart ----
axes[0, 0].plot(df["Date"], df["Sales"], color="blue", label="Sales")
axes[0, 0].plot(df["Date"], df["Profit"], color="green", label="Profit")
axes[0, 0].set_title("Sales & Profit Over Time")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Value")
axes[0, 0].legend()
axes[0, 0].grid(True, linestyle="--", alpha=0.5)
# Annotate highest sales point
max_idx = df["Sales"].idxmax()
axes[0, 0].annotate("Peak Sales",
                    xy=(df["Date"][max_idx], df["Sales"][max_idx]),
                    xytext=(df["Date"][max_idx], df["Sales"].max() + 10),
                    arrowprops=dict(facecolor='black', arrowstyle="->"))

# ---- 2. Scatter Plot with Color Mapping ----
scatter = axes[0, 1].scatter(df["Sales"], df["Profit"], c=df["Customers"],
                              cmap="viridis", edgecolor="k", alpha=0.8)
axes[0, 1].set_title("Sales vs Profit by Customers")
axes[0, 1].set_xlabel("Sales")
axes[0, 1].set_ylabel("Profit")
cbar = fig.colorbar(scatter, ax=axes[0, 1])
cbar.set_label("Number of Customers")

# ---- 3. Histogram ----
axes[1, 0].hist(df["Sales"], bins=15, color="orange", edgecolor="black")
axes[1, 0].set_title("Sales Distribution")
axes[1, 0].set_xlabel("Sales")
axes[1, 0].set_ylabel("Frequency")
axes[1, 0].grid(axis='y', linestyle="--", alpha=0.5)

# ---- 4. Box Plot ----
axes[1, 1].boxplot([df["Sales"], df["Profit"], df["Customers"]],
                   labels=["Sales", "Profit", "Customers"],
                   patch_artist=True,
                   boxprops=dict(facecolor="lightblue"))
axes[1, 1].set_title("Value Spread & Outliers")
axes[1, 1].grid(axis='y', linestyle="--", alpha=0.5)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
