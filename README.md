# Analyzing A/B Tests

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Features and Functions](#features-and-functions)
4. [Technologies Used](#technologies-used)
5. [How to Use](#how-to-use)

## Overview

This project involves analyzing the results of an A/B test conducted by a fast-food chain to evaluate the effectiveness of three different marketing campaigns. The aim is to determine which promotion strategy maximizes sales and to develop actionable insights through statistical testing and data visualization.

- **Dataset**: The dataset contains weekly sales data for different stores, categorized by promotions, market size, market ID, and other features. The target metric for evaluation is **SalesInThousands**, representing weekly sales in thousands of dollars for each store.

Key steps in the analysis include:

- **Data Exploration**:

  - Analyzing the distribution of sales data, identifying patterns such as right-skewed bimodal distribution and relationships between features like market size and sales.
  - Highlighting the sales performance differences across markets and promotions.

- **Statistical Testing**:

  - Checking assumptions for ANOVA and Tukey's HSD to ensure statistical validity, including tests for normality, homogeneity of variances, and independence.
  - Conducting ANOVA to assess whether there are significant differences in sales across the three promotions.
  - Applying Tukey's HSD for pairwise comparisons to pinpoint which promotions are significantly different from each other.

- **Results and Insights**:

  - Identifying **Promotion 2** as the least effective promotion due to significantly lower sales compared to **Promotion 1** and **Promotion 3**.
  - Concluding that **Promotion 1** is the most effective, based on mean sales and statistical comparisons.

- **Visualization**:
  - Creating dashboards and visual summaries to clearly communicate findings, including Tukey's HSD pairwise comparison results and confidence intervals for mean differences.

This project focuses on analyzing the results of an A/B test conducted by the creators of the **Cookie Cats** mobile game. The objective is to evaluate the impact of moving the first in-game gate from **level 30** to **level 40** on player behavior. Key performance metrics such as **retention rates** and **game rounds played** are used to assess the results of the test.

Key steps in the analysis include:

- **Data Cleaning**: Identifying and handling missing values and extreme outliers to ensure accurate and reliable analysis.
- **Exploratory Data Analysis (EDA)**: Examining the distribution of variables, identifying relationships between retention rates and gameplay metrics, and exploring group differences.
- **Statistical Testing**: Using statistical techniques like Chi-Square tests and t-tests to evaluate significant differences between the **gate_30** and **gate_40** groups.
- **Bootstrap Analysis**: Applying bootstrap methods to estimate confidence intervals and visualize the variability in metrics across groups.
- **Data Visualization**: Creating visualizations like histograms, boxplots, and confidence interval plots to effectively communicate findings.
- **Insights and Recommendations**: Drawing actionable insights from the analysis to recommend whether to adopt the **gate_40** version or retain the **gate_30** version.

The analysis aims to provide a data-driven recommendation by uncovering trends, evaluating retention rates, and understanding the gameplay impact of the gate change.

## Project Structure

The project directory contains the following files:

```
.
├── data/
│ ├── cookie_cats.csv
│ └── WA_Marketing-Campaign.csv
 ── src/
│ └── utils.py # Utility functions for data manipulation, cleaning, and visualization
├── fast_food_marketing_campaign.ipynb
├── fast_food_marketing_campaign_without_market3.ipynb
├── mobile_games_ab_testing-cookie_cats.ipynb
├── Fast_Food_Marketing_Campaign_Dashboard.pdf
├── .gitignore
├── README.md
└── requirements.txt

```

- **data**: Contains all the data files used in the project, including CSV, GeoJSON, and SQLite files.

  - `cookie_cats.csv`: contains data about two Cookie Cats mobile game versions.
  - `WA_Marketing-Campaign.csv`: contains information about a test conducted by a fast-food chain to evaluate three different promotions.

- **src**: Contains Python scripts used for various tasks like constants, database connections, and utility functions.

  - `utils.py`: Utility functions for data manipulation, cleaning, and visualization.

- **fast_food_marketing_campaign.ipynb**: A/B test for different promotions.
- **fast_food_marketing_campaign_without_market3.ipynb**: A/B test for different promotions without MarketID=3.
- **mobile_games_ab_testing-cookie_cats.ipynb**: A/B test for different game versions.
- **Fast_Food_Marketing_Campaign_Dashboard.pdf**: Fast Food Marketing Campaign Dashboard.

- **.gitignore**: Specifies the files and directories to ignore in version control.
- **README.md**: Provides an overview of the project, its goals, and how to use it.
- **requirements.txt**: Lists all required Python dependencies for the project.

## Features and Functions

The project includes several key features and functions for data analysis:

### Data Cleaning and Transformation Functions

- **`print_list(list_to_print: list)`**: Prints each item in a given list.
- **`encode_feature_from_list(df: pd.DataFrame, encode_feature: str)`**: Encodes a feature containing lists into separate binary columns.
- **`encode_categorical_features(df: pd.DataFrame, categorical_features: list)`**: One-hot encodes categorical features in a DataFrame.

### Outlier Detection and Data Distribution Visualization

- **`find_outliers(df: pd.DataFrame, col: str, outliers_num: int = 5)`**: Identifies outliers in a specific column using the IQR method.
- **`plot_categorical_distribution(df: pd.DataFrame, feature: str, show: bool = True, color: str = "#3174A1")`**: Plots the distribution of a categorical feature.
- **`plot_numeric_distribution(df: pd.DataFrame, feature: str, bins: int = 20, hue: str = None)`**: Plots the distribution of a numeric feature.
- **`plot_box(df: pd.DataFrame, col: str)`**: Creates a boxplot to visualize outliers in a specified column.
- **`plot_barchart(data: pd.DataFrame, x_col: str, y_col: str, vertical: bool = True, subplots: bool = False, show_values: bool = False, color: str = "#3174A1")`**: Creates a bar chart for a given DataFrame.
- **`plot_box_with_category(df: pd.DataFrame, numeric_feature: str, feature: str)`**: Creates a boxplot of a numeric feature grouped by a categorical feature.

### Data Aggregation and Grouping

- **`count_group_total_percentage(df: pd.DataFrame, feature_1: str, feature_2: str)`**: Calculates the count, total, and percentage for grouped categories in a DataFrame.
- **`count_prevalence_rate(df: pd.DataFrame, conditions: list)`**: Calculates prevalence rates and confidence intervals for conditions.

### Advanced Visualization Functions

- **`subplot_two_categorical_distribution(df: pd.DataFrame, feature_1: str, feature_2: str)`**: Plots side-by-side distributions of two categorical features.
- **`subplot_two_categorical_features(df: pd.DataFrame, feature_1: str, feature_2: str, y_col: str)`**: Creates subplots to visualize the relationship between two categorical features.
- **`create_world_map(data_dict: dict)`**: Creates a world map with country-level data distribution.
- **`create_us_map(state_dict: dict, state_dict_percentage: dict)`**: Creates a US map with state-level data and percentages.

### Correlation and Statistical Analysis

- **`cramers_v(x: pd.Series, y: pd.Series)`**: Calculates Cramér's V statistic for categorical-categorical association.
- **`categorical_correlation_matrix(df: pd.DataFrame)`**: Computes a correlation matrix for categorical features.
- **`plot_heatmap(corr_matrix: pd.DataFrame, linewidths: int = 0, figsize: tuple = (10, 8), fmt: str = ".2f", title: str = "")`**: Plots a heatmap for a given correlation matrix.
- **`categorical_and_numeric_correlation(df: pd.DataFrame, numeric_feature: str, categorical_columns: list)`**: Computes ANOVA p-values for numeric-categorical feature pairs.

### Additional Statistical Functions

- **`plot_prevalence_rate(df: pd.DataFrame)`**: Plots prevalence rates with confidence intervals for conditions.

## Technologies Used

- **Python 3.x**: The primary programming language used for analysis.
- **pandas**: For data manipulation and cleaning.
- **matplotlib**: For generating plots and visualizations.
- **seaborn**: For creating statistical visualizations like boxplots and correlation heatmaps.
- **scikit-learn**: For scaling data and preprocessing.
- **statsmodels**: For statistical analysis.
- **folium**: For creating interactive maps.
- **shapely**: For geometric operations on map data.
- **scipy**: For statistical analysis and calculations.
- **ast**: For parsing literal expressions in strings.
- **json**: For working with JSON data.

## How to Use

### Prerequisites

- Python 3.8 or later
- `pip` for managing Python packages

### Installation

1. Clone the repository:

   ```bash
    git clone <repository-url>
    cd <module-folder>

    python -m venv venv
    venv\Scripts\activate

    pip install -r requirements.txt
   ```
