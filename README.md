# 📊 Multidimensional Climate & Hydrology Visualizations

Welcome!  This project offers a concise yet lively exploration of three real‑world datasets related to weather and climate.  The aim is simple: **turn raw tables into pictures** that tell a story about patterns across many dimensions — time, space, temperature, humidity and more.  A Python script in `src/create_visualizations.py` does the heavy lifting, reading the CSVs in `data/`, producing figures with familiar libraries like `pandas`, `matplotlib` and `seaborn`, and saving them to `output/`.  Here’s a quick peek at the directory layout:

```text
data_visualization_assignment2/
├── data/                # CSV files used for the visualizations
│   ├── weather_data.csv             # Daily weather for several cities
│   ├── global_temp.csv              # NASA GISTEMP land–ocean anomalies (raw)
│   └── minnesota_weather.csv        # Monthly weather summaries for 6 Minnesota sites
├── src/
│   └── create_visualizations.py     # Script that generates the figures
└── output/             # Generated charts
    ├── weather_heatmap.png
    ├── weather_scatter.png
    ├── global_temp_heatmap.png
    └── minnesota_precip_line.png
```

## Datasets and why they were chosen

**Daily weather for multiple world cities (mosaicData)** –  *weather_data.csv* is derived from the `Weather` dataset in the `mosaicData` package.  According to the official documentation this table contains **2016–2017 daily weather observations for several world cities**, including variables such as city, date, high/average/low temperature, dew point, humidity, sea‑level pressure, visibility, wind speed, precipitation and weather events【209500219273106†L78-L137】.  Temperatures are recorded in degrees Fahrenheit and precipitation is given as a character value (e.g. `T` for a trace amount)【209500219273106†L108-L135】.  The data were scraped from WeatherUnderground in January 2018【209500219273106†L140-L143】.  This dataset was attractive because it provides daily values for multiple variables across a range of climates—from tropical Mumbai to temperate Auckland and Chicago—and thus allows several dimensions (city, time, temperature, humidity, precipitation) to be combined in one graphic.

**Global land–ocean temperature anomalies (NASA GISTEMP)** –  *global_temp.csv* is a CSV copy of the `GLB.Ts+dSST.csv` file from NASA’s GISTEMP (v4) analysis.  The GISTEMP project combines NOAA’s Global Historical Climatology Network (GHCN v4) station data with ERSST v5 sea‑surface temperatures to estimate the change in global surface temperature【238077913597605†L30-L38】.  Anomalies are expressed relative to the **1951–1980** mean and represent deviations in °C【57940960815465†L124-L139】.  The dataset provides monthly anomalies from **1880–2025** and is updated around the 10th of each month【238077913597605†L30-L38】.  Long‑term temperature records are fundamental to hydrology and climate change research, and the monthly time resolution allows the warming trend to be visualised across both years and seasons.

**Minnesota barley trial weather summary (agridat)** –  *minnesota_weather.csv* comes from the `minnesota.barley.weather` dataset in the `agridat` package.  It contains **monthly weather summaries from 1927–1936 for six sites in Minnesota** where barley yield trials were conducted【635360545156382†L22-L59】.  Variables include the site name, year, month, cooling degree days (cdd), heating degree days (hdd), precipitation (inches), and average daily minimum and maximum temperature (°F)【635360545156382†L22-L59】.  The data were extracted from National Climate Data Center records【635360545156382†L63-L86】.  This dataset was chosen to contrast the global perspective with a local regional climate over a decade and to explore how precipitation varied among nearby sites.

## 🛠️ Generating the visualizations

The `create_visualizations.py` script loads these CSV files using `pandas` and then constructs the following visualizations:

### 1. 🌡️ Average monthly temperature by city (heatmap)

This heatmap aggregates the daily weather data into mean monthly temperatures for each city.  Grouping by month and city and then pivoting the table yields a matrix of average temperatures.  A divergent `coolwarm` colour palette highlights high values in red and low values in blue.  Annotating each cell with the value makes the numeric differences explicit.  The colour bar is labelled *“Average temperature”* to reflect the underlying Fahrenheit values【209500219273106†L108-L135】, and months are ordered from 1 to 12.  Heatmaps are effective for showing patterns across two categorical dimensions; here they reveal that Beijing and Chicago have large seasonal swings (winter temperatures near freezing and summer peaks near 80 °F), Auckland has a mild maritime climate with temperatures between 50–70 °F year‑round, San Diego remains temperate, and Mumbai stays above 70 °F throughout the year.  A caption is included beneath the figure in the final report.

### 2. 🌬️💧 Daily temperature vs humidity with precipitation encoding (scatter plot)

To explore relationships between multiple variables in the daily weather data, a scatter plot was used.  Each point represents a day; the *x*–axis shows average relative humidity, the *y*–axis shows average temperature (still in °F), the marker colour encodes the city and the marker size encodes precipitation (trace amounts have been set to zero).  A scatter allows one to see whether warmer days tend to be more humid and whether large precipitation events coincide with particular temperature–humidity combinations.  The plot shows that Mumbai and Auckland have higher humidity and precipitation overall, whereas Beijing and Chicago feature lower humidity during cool months and little precipitation.  Precipitation events are visible as larger markers clustered at moderate humidity values.  Legends for colour and size are placed outside the plot to avoid occluding data.

### 3. 🔥🧊 Global temperature anomalies heatmap

For the GISTEMP dataset the script first skips the descriptive header line and converts `***` entries to missing values.  The monthly anomaly columns are melted into long format and then pivoted back into a Year × Month matrix.  A heatmap with a `coolwarm` palette displays anomalies from −1.5 °C to +1.5 °C relative to the 1951–1980 baseline【57940960815465†L124-L139】.  Blue shades indicate temperatures cooler than the baseline, red shades indicate warmer conditions.  This visualization clearly shows the gradual warming of the planet: early decades (1880s–1930s) are predominantly blue, mid‑century decades transition to neutral colours, and the most recent decades (1980s onward) are dominated by red.  The strongest warming appears in the last decade (2010s–2020s), with 2016 and 2020 standing out as particularly warm years.  The x‑axis labels use month abbreviations for clarity and the y‑axis lists each year from 1880 onward.  Such a dense matrix is best interpreted visually rather than with textual tables; patterns across both seasonal and multi‑decadal scales emerge at a glance.

### 4. 🌧️ Monthly precipitation by Minnesota site (line chart)

The Minnesota barley data were used to examine how precipitation varied across sites over a ten‑year period.  A line chart was selected because it conveys temporal trends effectively.  The script creates a date column from the year and month and then plots precipitation (in inches) against this date, with separate lines for each site.  A legend identifies the sites, and a tight layout keeps the plot compact.  The figure shows that precipitation peaks in the summer months (June–August) for all sites, reflecting the continental climate of Minnesota, and that Waseca and St Paul tend to receive more precipitation than Morris or Crookston.  An absence of data for Duluth in December 1931 is evident as a gap in the line【635360545156382†L76-L81】.

## 💡 Choices, challenges and future work

### 🎨 Why these visualisations?

The main objective was to illustrate multi‑dimensional patterns using simple yet informative graphics.  Heatmaps were chosen for the first and third visualisations because they compactly summarise two categorical dimensions (city × month or year × month) and encode a quantitative variable using colour; this makes them ideal for identifying seasonal cycles and long‑term trends.  The scatter plot allowed us to encode three variables—temperature, humidity and precipitation—within a single panel by mapping precipitation to marker size and city to colour.  The line chart emphasised temporal continuity and allowed comparison across multiple sites on the same scale.  Using `seaborn` simplified the construction of these plots, while `pandas` handled data wrangling efficiently.

### 🔭 What could be improved?

There are several ways this project could be extended.  For the daily weather data we would like to convert all temperature and precipitation units consistently, perhaps expressing temperatures in °C to match the GISTEMP anomalies and computing precipitation amounts from the `T` (trace) codes.  Interactive tools such as `plotly` or `Altair` could allow users to hover over individual points, filter by city or season, and explore specific days in detail.  When working with the GISTEMP dataset we limited ourselves to a simple heatmap; more advanced techniques (e.g., principal component analysis or clustering) could be used to group years with similar anomaly patterns and examine regional contributions to the global signal.  For the Minnesota barley data it would be insightful to combine the weather summary with yield data to explore how cooling and heating degree days influence barley yields; this would require joining with the `minnesota.barley.yield` dataset and fitting regression models.  Finally, developing a web‑based dashboard that links these datasets could provide an integrated view of weather and climate patterns across scales.

## 🏗️ How to reproduce

1. Ensure you have Python 3 with the following packages installed: `pandas`, `matplotlib`, `seaborn` and `numpy` 📚.  A virtual environment makes it easy to manage dependencies.
2. Run `python src/create_visualizations.py` from the root of this repository.  The script will load the data files from the `data/` directory and write four image files into `output/`.  Each figure is saved at 300 dpi for inclusion in reports.
3. Review the figures in the `output/` directory.  The descriptive captions above summarise the main insights.  You can experiment with alternative chart types or modify the script to explore other variables.

---

**Citation notes:**  The descriptions of the `Weather` and `minnesota.barley.weather` datasets are taken from their official R package documentation, which clarifies variable definitions and data sources【209500219273106†L78-L137】【635360545156382†L22-L59】.  Information about the GISTEMP dataset—including the combination of GHCN v4 station data with ERSST v5 sea‑surface temperatures and the 1951–1980 baseline—is drawn from NASA and NOAA documentation【238077913597605†L30-L38】【57940960815465†L124-L139】.  These sources explain the provenance and interpretation of the datasets used here.