# weatherdatavisualiser.py
# Name:Rishabh Bhardwaj
#Rollno- 2501730355
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------
# TASK 1: LOAD DATA
# ---------------------------------------------------

def load_data(file_path):
    df = pd.read_csv(file_path)
    print("\n--- RAW DATA HEAD ---")
    print(df.head())
    print("\n--- INFO ---")
    print(df.info())
    print("\n--- DESCRIPTION ---")
    print(df.describe())
    return df


# ---------------------------------------------------
# TASK 2: CLEANING
# ---------------------------------------------------

def clean_data(df):
    # Convert date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Remove rows where date is invalid
    df = df.dropna(subset=['date'])

    # Handle missing values for numeric columns
    num_cols = ['temperature', 'rainfall', 'humidity']
    df[num_cols] = df[num_cols].fillna(df[num_cols].mean())

    # Keep only relevant columns
    df = df[['date', 'temperature', 'rainfall', 'humidity']]

    print("\n--- CLEANED DATA SAMPLE ---")
    print(df.head())
    return df


# ---------------------------------------------------
# TASK 3: STATISTICS USING NUMPY
# ---------------------------------------------------

def compute_stats(df):
    temps = df['temperature'].values
    print("\n--- TEMPERATURE STATS ---")
    print("Mean:", np.mean(temps))
    print("Min:", np.min(temps))
    print("Max:", np.max(temps))
    print("Standard Deviation:", np.std(temps))


# ---------------------------------------------------
# TASK 4: VISUALIZATION
# ---------------------------------------------------

def create_plots(df):
    # Line plot: Temperature trend
    plt.figure(figsize=(8, 4))
    plt.plot(df['date'], df['temperature'])
    plt.title("Daily Temperature Trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature")
    plt.tight_layout()
    plt.savefig("temperature_trend.png")
    plt.close()

    # Bar chart: Monthly rainfall
    df['month'] = df['date'].dt.month
    monthly_rain = df.groupby('month')['rainfall'].sum()

    plt.figure(figsize=(8, 4))
    plt.bar(monthly_rain.index, monthly_rain.values)
    plt.title("Monthly Rainfall")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.tight_layout()
    plt.savefig("monthly_rainfall.png")
    plt.close()

    # Scatter plot: Humidity vs Temperature
    plt.figure(figsize=(6, 4))
    plt.scatter(df['temperature'], df['humidity'])
    plt.title("Humidity vs Temperature")
    plt.xlabel("Temperature")
    plt.ylabel("Humidity")
    plt.tight_layout()
    plt.savefig("humidity_vs_temperature.png")
    plt.close()

    # Combined subplot
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    # Left subplot: Temperature line
    ax[0].plot(df['date'], df['temperature'])
    ax[0].set_title("Temperature Trend")
    ax[0].set_xlabel("Date")
    ax[0].set_ylabel("Temperature")

    # Right subplot: Humidity scatter
    ax[1].scatter(df['temperature'], df['humidity'])
    ax[1].set_title("Humidity vs Temperature")
    ax[1].set_xlabel("Temperature")
    ax[1].set_ylabel("Humidity")

    plt.tight_layout()
    plt.savefig("combined_plots.png")
    plt.close()

    print("\nPlots saved as PNG files!")


# ---------------------------------------------------
# TASK 5: GROUPING AND AGGREGATION
# ---------------------------------------------------

def monthly_stats(df):
    df['month'] = df['date'].dt.to_period('M')
    grouped = df.groupby('month').mean()[['temperature', 'rainfall', 'humidity']]
    print("\n--- MONTHLY AVERAGES ---")
    print(grouped)
    return grouped


# ---------------------------------------------------
# TASK 6: EXPORT CLEANED DATA
# ---------------------------------------------------

def export_cleaned(df):
    df.to_csv("cleaned_weather.csv", index=False)
    print("\nCleaned weather data saved as cleaned_weather.csv")


# ---------------------------------------------------
# MAIN WORKFLOW
# ---------------------------------------------------

def main():
    file_path = "weather.csv"   # Change if your CSV has a different name

    df = load_data(file_path)
    df = clean_data(df)
    compute_stats(df)
    create_plots(df)
    monthly_stats(df)
    export_cleaned(df)

    print("\nAll tasks completed successfully!")


main()
