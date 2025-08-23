import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


filename = r'climate2.csv'
with open(filename) as file:
   data = csv.DictReader(file)

df = pd.read_csv(filename)
# print (df["datetime_ist"])
# Convert datetime column
df["datetime_ist"] = pd.to_datetime(df["datetime_ist"])
# plt.style.use("seaborn-v0_8-whitegrid")
fig, axes = plt.subplots(6, 2, figsize=(20,18))
axes = axes.flatten()

# 1. Temperature trend
axes[0].plot(df["datetime_ist"], df["temperature_c"], color="tomato")
axes[0].set_title("Temperature Trend")

# 2. Humidity trend
axes[1].plot(df["datetime_ist"], df["humidity_pct"], color="royalblue")
axes[1].set_title("Humidity Trend")

# 3. Rainfall trend
axes[2].bar(df["datetime_ist"], df["rainfall_mm"], color="seagreen", alpha=0.6)
axes[2].set_title("Rainfall Trend")

# 4. Pressure trend
axes[3].plot(df["datetime_ist"], df["pressure_hpa"], color="purple")
axes[3].set_title("Pressure Trend")

# 5. Wind speed trend
axes[4].plot(df["datetime_ist"], df["wind_speed_kmh"], color="orange")
axes[4].set_title("Wind Speed Trend")

# 6. Wind direction scatter
axes[5].scatter(df["datetime_ist"], df["wind_direction_deg"], s=5, color="gray")
axes[5].set_title("Wind Direction Over Time")

# 7. Temperature distribution
axes[6].hist(df["temperature_c"], bins=20, color="tomato", edgecolor="black")
axes[6].set_title("Temperature Distribution")

# 8. Humidity distribution
axes[7].hist(df["humidity_pct"], bins=20, color="royalblue", edgecolor="black")
axes[7].set_title("Humidity Distribution")

# 9. Rainfall distribution
axes[8].hist(df["rainfall_mm"], bins=20, color="seagreen", edgecolor="black")
axes[8].set_title("Rainfall Distribution")

# 10. Boxplot comparison
axes[9].boxplot(
    [df["temperature_c"], df["humidity_pct"], df["rainfall_mm"]],
    labels=["Temp (°C)", "Humidity (%)", "Rainfall (mm)"],
    patch_artist=True
)
axes[9].set_title("Boxplot Comparison")

# Formatting
for ax in axes[:6]:  # time series plots
    ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.show()