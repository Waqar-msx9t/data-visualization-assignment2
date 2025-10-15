"""
Script to generate multi‑dimensional data visualizations for the
CMP_SC‑8630 data visualization assignment.  The script loads three
real‑world datasets related to climate and hydrology and produces
visualizations that explore patterns across multiple variables and
dimensions.  The resulting figures are saved to the ``output``
directory.  The datasets used here include:

* ``weather_data.csv`` – daily weather observations for multiple
  cities in New Zealand (2016–2017) containing temperature,
  humidity, wind, pressure and precipitation variables.  Source:
  mosaicData package within the Rdatasets collection.
* ``global_temp.csv`` – NASA Goddard Institute for Space Studies
  (GISTEMP) global land–ocean temperature anomalies from 1880 to
  2025.  Monthly anomalies relative to the 1951–1980 baseline are
  provided.  Source: NASA GISS via data.giss.nasa.gov.
* ``minnesota_weather.csv`` – monthly weather summary for six
  Minnesota agricultural sites (1927–1936) including cooling and
  heating degree days, precipitation and temperature extremes.
  Source: agridat package within Rdatasets.

The visualizations include heatmaps, scatter plots and line charts
to illustrate how variables such as temperature, humidity and
precipitation vary over time and across different locations.
"""

import os
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def ensure_output_dir(path: str) -> None:
    """Ensure that the output directory exists."""
    os.makedirs(path, exist_ok=True)


def plot_weather_heatmap(df: pd.DataFrame, outdir: str) -> str:
    """Create a heatmap of average temperature by city and month.

    Parameters
    ----------
    df : pandas.DataFrame
        Weather data with columns ``city``, ``month`` and ``avg_temp``.
    outdir : str
        Directory to write the output image.

    Returns
    -------
    str
        Path to the saved figure.
    """
    # Compute monthly mean temperatures for each city
    monthly_avg = (
        df.groupby(["city", "month"]) ["avg_temp"]
        .mean()
        .reset_index()
    )
    # Pivot to create city × month matrix
    pivot_table = monthly_avg.pivot(index="city", columns="month", values="avg_temp")
    # Sort months in calendar order
    pivot_table = pivot_table.sort_index(axis=1)

    # Plot heatmap
    plt.figure(figsize=(10, 4))
    sns.heatmap(
        pivot_table,
        cmap="coolwarm",
        cbar_kws={"label": "Average temperature"},
        annot=True,
        fmt=".1f"
    )
    plt.title("Average monthly temperature by city")
    plt.xlabel("Month")
    plt.ylabel("City")
    plt.tight_layout()
    fname = os.path.join(outdir, "weather_heatmap.png")
    plt.savefig(fname, dpi=300)
    plt.close()
    return fname


def plot_weather_scatter(df: pd.DataFrame, outdir: str) -> str:
    """Create a scatter plot exploring relationships between humidity,
    temperature and precipitation.

    Each point represents a daily observation.  The x‑axis shows
    average humidity, the y‑axis shows average temperature in Fahrenheit,
    the marker size encodes precipitation and colour encodes the city.
    Separate legends are provided for city and precipitation to avoid
    overlap.

    Parameters
    ----------
    df : pandas.DataFrame
        Weather data with columns ``avg_humidity``, ``avg_temp``,
        ``precip`` and ``city``.
    outdir : str
        Directory to write the output image.

    Returns
    -------
    str
        Path to the saved figure.
    """
    # Replace missing precipitation with zero for plotting
    df_plot = df.copy()
    # Convert precipitation to numeric: replace strings like 'T' or empty with NaN,
    # then coerce to floats and fill missing values with zero.
    df_plot["precip"] = pd.to_numeric(df_plot["precip"], errors="coerce").fillna(0.0)

    # Compute a reasonable scaling for precipitation sizes
    max_precip = df_plot["precip"].quantile(0.95) if df_plot["precip"].notna().any() else 1.0
    # Bound size range to avoid huge markers
    size_range = (20, 300)

    plt.figure(figsize=(9, 6))
    # Use a distinct palette with as many colours as there are cities
    palette = sns.color_palette(n_colors=df_plot["city"].nunique())
    ax = sns.scatterplot(
        data=df_plot,
        x="avg_humidity",
        y="avg_temp",
        hue="city",
        size="precip",
        sizes=size_range,
        alpha=0.65,
        palette=palette,
        legend=False,
    )
    ax.set_xlabel("Average relative humidity (%)")
    ax.set_ylabel("Average temperature (°F)")
    ax.set_title("Daily weather: temperature vs humidity with precipitation (size)")

    # Create separate legends: one for city colours and one for precipitation sizes
    from matplotlib.lines import Line2D
    city_names = list(dict.fromkeys(df_plot["city"]))
    color_map = {c: palette[i % len(palette)] for i, c in enumerate(city_names)}
    city_handles = [
        Line2D(
            [0], [0], marker="o", color="w", label=c,
            markerfacecolor=color_map[c], markersize=8, markeredgecolor="black", alpha=0.9
        )
        for c in city_names
    ]
    leg1 = ax.legend(handles=city_handles, title="City", loc="upper left", bbox_to_anchor=(1.02, 1.0))
    ax.add_artist(leg1)

    # Legend for precipitation sizes using representative quantiles
    ref_values = np.unique(np.round(np.linspace(0, max_precip, 4), 2))
    size_handles = [
        plt.scatter(
            [], [], s=np.interp(v, [0, max_precip], size_range), facecolor="gray",
            edgecolor="black", alpha=0.6
        )
        for v in ref_values
    ]
    leg2 = ax.legend(size_handles, [f"{v:g}" for v in ref_values], title="Precipitation", loc="lower left", bbox_to_anchor=(1.02, 0.0))
    plt.tight_layout()
    fname = os.path.join(outdir, "weather_scatter.png")
    plt.savefig(fname, dpi=300)
    plt.close()
    return fname


def plot_global_temp_heatmap(df: pd.DataFrame, outdir: str) -> str:
    """Create a heatmap of global temperature anomalies by year and month.

    Parameters
    ----------
    df : pandas.DataFrame
        Global temperature anomalies where rows correspond to years and
        columns to months (Jan–Dec).  The DataFrame should include
        numeric values for anomalies.  Missing values are allowed and
        will appear as blank cells.
    outdir : str
        Directory to write the output image.

    Returns
    -------
    str
        Path to the saved figure.
    """
    # Melt the monthly columns into long format
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"
    ]
    df_long = df.melt(id_vars="Year", value_vars=months, var_name="Month", value_name="Anomaly")
    # Convert month names to numbers for correct ordering
    month_order = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    df_long["MonthNum"] = df_long["Month"].map(month_order)
    # Pivot to Year × Month matrix
    heatmap_data = df_long.pivot(index="Year", columns="MonthNum", values="Anomaly")
    # Sort by year ascending
    heatmap_data = heatmap_data.sort_index()
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        heatmap_data,
        cmap="coolwarm",
        cbar_kws={"label": "Temperature anomaly (°C relative to 1951–1980)"},
        vmin=-1.5,
        vmax=1.5,
        linewidths=0,
        linecolor="white"
    )
    plt.title("Global land–ocean temperature anomalies (1880–2025)")
    plt.xlabel("Month")
    plt.ylabel("Year")
    # Replace x axis labels with month abbreviations
    plt.xticks(
        ticks=range(1, 13),
        labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        rotation=45
    )
    plt.tight_layout()
    fname = os.path.join(outdir, "global_temp_heatmap.png")
    plt.savefig(fname, dpi=300)
    plt.close()
    return fname


def plot_minnesota_precip_line(df: pd.DataFrame, outdir: str) -> str:
    """Create a line chart of monthly precipitation by site over time.

    This figure shows how precipitation varies across the six Minnesota
    sites from 1927 to 1936.  Each line corresponds to a site and
    month; values are aggregated by year and month.

    Parameters
    ----------
    df : pandas.DataFrame
        Minnesota weather data with columns ``site``, ``year``, ``mo`` (month) and
        ``precip``.
    outdir : str
        Directory to write the output image.

    Returns
    -------
    str
        Path to the saved figure.
    """
    # Create a date column for plotting
    df_plot = df.copy()
    df_plot["date"] = pd.to_datetime(dict(year=df_plot["year"], month=df_plot["mo"], day=1))
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_plot, x="date", y="precip", hue="site")
    plt.xlabel("Year")
    plt.ylabel("Precipitation (inches)")
    plt.title("Monthly precipitation by Minnesota site (1927–1936)")
    plt.legend(title="Site", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    fname = os.path.join(outdir, "minnesota_precip_line.png")
    plt.savefig(fname, dpi=300)
    plt.close()
    return fname


def main() -> List[str]:
    """Run all visualizations and return a list of generated file paths."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    out_dir = os.path.join(base_dir, "output")
    ensure_output_dir(out_dir)
    figures: List[str] = []

    # Load and plot weather data
    weather_path = os.path.join(data_dir, "weather_data.csv")
    weather_df = pd.read_csv(weather_path)
    # Plot heatmap and scatter
    figures.append(plot_weather_heatmap(weather_df, out_dir))
    figures.append(plot_weather_scatter(weather_df, out_dir))

    # Load and plot global temperature anomalies
    global_path = os.path.join(data_dir, "global_temp.csv")
    global_df = pd.read_csv(global_path, skiprows=1)
    # Replace *** with NA and convert to numeric
    global_df = global_df.replace("***", pd.NA)
    for col in global_df.columns[1:]:
        global_df[col] = pd.to_numeric(global_df[col], errors="coerce")
    figures.append(plot_global_temp_heatmap(global_df, out_dir))

    # Load and plot Minnesota weather data
    minn_path = os.path.join(data_dir, "minnesota_weather.csv")
    minn_df = pd.read_csv(minn_path)
    figures.append(plot_minnesota_precip_line(minn_df, out_dir))
    return figures


if __name__ == "__main__":
    generated = main()
    print("Generated figures:")
    for path in generated:
        print(path)