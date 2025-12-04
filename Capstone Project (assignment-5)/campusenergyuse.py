# capmusenergyuse.py
# Name:Rishabh Bhardwaj
#Rollno- 2501730355
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# TASK 3 — OOP CLASSES
# ============================================================

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        avg = np.mean([r.kwh for r in self.meter_readings])
        return {
            "building": self.name,
            "total_kwh": total,
            "avg_kwh": avg,
            "num_readings": len(self.meter_readings)
        }


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_reading(self, building_name, timestamp, kwh):
        if building_name not in self.buildings:
            self.buildings[building_name] = Building(building_name)
        reading = MeterReading(timestamp, kwh)
        self.buildings[building_name].add_reading(reading)

    def generate_all_reports(self):
        return [b.generate_report() for b in self.buildings.values()]


# ============================================================
# TASK 1 — LOAD & VALIDATE MULTIPLE CSV FILES
# ============================================================

def load_all_data(data_folder="data"):
    folder = Path(data_folder)
    all_rows = []

    for file in folder.glob("*.csv"):
        try:
            df = pd.read_csv(file)
            df["building"] = file.stem  # filename as building name
            all_rows.append(df)
        except Exception as e:
            print(f"Error loading {file}: {e}")

    if not all_rows:
        raise Exception("No valid CSV files found in /data directory!")

    df_combined = pd.concat(all_rows, ignore_index=True)

    # Clean timestamp
    df_combined["timestamp"] = pd.to_datetime(df_combined["timestamp"], errors="coerce")
    df_combined = df_combined.dropna(subset=["timestamp", "kwh"])

    print("Combined Data Loaded:")
    print(df_combined.head())

    return df_combined


# ============================================================
# TASK 2 — CORE AGGREGATIONS
# ============================================================

def calculate_daily_totals(df):
    df = df.set_index("timestamp")
    return df.resample("D")["kwh"].sum()


def calculate_weekly_aggregates(df):
    df = df.set_index("timestamp")
    return df.resample("W")["kwh"].sum()


def building_wise_summary(df):
    summary = df.groupby("building")["kwh"].agg(["mean", "min", "max", "sum"])
    return summary


# ============================================================
# TASK 4 — VISUALIZATIONS
# ============================================================

def create_dashboard_plot(df_daily, df_weekly, df_building):
    fig, ax = plt.subplots(1, 3, figsize=(18, 5))

    # ---- Plot 1: Daily Trend Line ----
    ax[0].plot(df_daily.index, df_daily.values)
    ax[0].set_title("Daily Electricity Consumption")
    ax[0].set_xlabel("Date")
    ax[0].set_ylabel("kWh")

    # ---- Plot 2: Weekly Bar Chart ----
    ax[1].bar(df_weekly.index.astype(str), df_weekly.values)
    ax[1].set_title("Weekly Energy Usage")
    ax[1].set_xlabel("Week")
    ax[1].set_ylabel("kWh")
    ax[1].tick_params(axis='x', rotation=45)

    # ---- Plot 3: Building Summary Scatter Plot ----
    ax[2].scatter(df_building["mean"], df_building["max"])
    for name in df_building.index:
        ax[2].annotate(name, (df_building.loc[name, "mean"], df_building.loc[name, "max"]))
    ax[2].set_title("Peak vs Avg Usage (Per Building)")
    ax[2].set_xlabel("Average kWh")
    ax[2].set_ylabel("Max kWh")

    plt.tight_layout()
    plt.savefig("dashboard.png")
    plt.close()

    print("Dashboard plot saved as dashboard.png")


# ============================================================
# TASK 5 — EXPORT CLEAN DATA + SUMMARY REPORT
# ============================================================

def export_outputs(df_clean, summary_table):
    df_clean.to_csv("cleaned_energy_data.csv", index=False)
    summary_table.to_csv("building_summary.csv")

    # Create summary report
    total_consumption = df_clean["kwh"].sum()
    highest_building = summary_table["sum"].idxmax()

    with open("summary.txt", "w") as f:
        f.write("===== CAMPUS ENERGY SUMMARY =====\n\n")
        f.write(f"Total Campus Consumption: {total_consumption:.2f} kWh\n")
        f.write(f"Highest Consuming Building: {highest_building}\n")
        f.write("\nBuilding Summary Table:\n")
        f.write(summary_table.to_string())

    print("Output files created: cleaned_energy_data.csv, building_summary.csv, summary.txt")


# ============================================================
# MAIN WORKFLOW
# ============================================================

def main():
    print("\n===== CAMPUS ENERGY DASHBOARD RUNNING =====\n")

    # Task 1: Load
    df = load_all_data("data")

    # Task 2: Aggregations
    df_daily = calculate_daily_totals(df)
    df_weekly = calculate_weekly_aggregates(df)
    summary = building_wise_summary(df)

    # Task 3: Feed OOP Model
    manager = BuildingManager()
    for _, row in df.iterrows():
        manager.add_reading(row["building"], row["timestamp"], row["kwh"])

    building_reports = manager.generate_all_reports()
    print("\nOOP Reports:")
    print(building_reports)

    # Task 4: Dashboard Visualization
    create_dashboard_plot(df_daily, df_weekly, summary)

    # Task 5: Export all files
    export_outputs(df, summary)

    print("\n===== ALL TASKS COMPLETED SUCCESSFULLY =====")


# Run Program
if __name__ == "__main__":
    main()
