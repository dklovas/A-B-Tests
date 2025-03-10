import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportion_confint
from sklearn.preprocessing import OneHotEncoder
import scipy.stats as stats
import ast
import folium
import json
from shapely.geometry import shape


def print_list(list_to_print: list) -> None:
    """
    Print each item in a list.

    Parameters:
        list_to_print (list): The list of items to print.

    Returns:
        None
    """

    for item in list_to_print:
        print(f"   - {item}")


def find_outliers(df: pd.DataFrame, col: str, outliers_num: int = 5) -> pd.DataFrame:
    """
    Identify outliers in a specific column of a DataFrame using the IQR method.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        col (str): The column name to check for outliers.
        outliers_num (int, optional): The number of outliers to return. Defaults to 5.

    Returns:
        pd.DataFrame: A DataFrame containing the top outliers.
    """
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (
        df.query(f"{col} < {lower_bound} or {col} > {upper_bound}")
        .sort_values(col)
        .tail(outliers_num)
    )


def plot_categorical_distribution(
    df: pd.DataFrame, feature: str, show: bool = True, color: str = "#3174A1"
) -> None:
    """
    Plot the distribution of a categorical feature in a DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        feature (str): The categorical feature to plot.
        show (bool, optional): Whether to display the plot. Defaults to True.
        color (str, optional): Color for the bars. Defaults to '#3174A1'.

    Returns:
        None
    """

    ax = sns.countplot(x=feature, data=df, edgecolor="black", color=color)
    plt.title(f"{feature.replace('_', ' ').title()} Distribution")

    for spine_name, spine in ax.spines.items():
        if spine_name != "bottom":
            spine.set_visible(False)
    ax.grid(axis="y", visible=False)

    plt.xlabel(feature.replace("_", " ").title())
    plt.ylabel("Count")
    plt.xticks(rotation=0)

    if show:
        plt.show()


def plot_numeric_distribution(
    data: pd.DataFrame, feature: str, bins: int = 20, hue: str = None, xlim: tuple = None, subplots=False, **kwargs
) -> None:
    """
    Plot the distribution of a numeric feature in a DataFrame.

    Parameters:
        data (pd.DataFrame): The input DataFrame.
        feature (str): The numeric feature to plot.
        bins (int, optional): Number of bins for the histogram. Defaults to 20.
        hue (str, optional): Additional variable to separate the data by. Defaults to None.
        xlim (tuple): The limits for the x-axis (optional). Format: (min, max)

    Returns:
        None
    """

    ax = sns.histplot(
        data=data, x=feature, kde=True, bins=bins, multiple="stack", edgecolor="black"
    )

    ax.set_title(f"{feature.replace('_', ' ').title()} Distribution")
    ax.set_xlabel(feature.replace("_", " ").title())
    ax.set_ylabel("Count")
    ax.yaxis.set_visible(True)
    sns.despine(left=True, ax=ax)

    if xlim:
        plt.xlim(xlim)

    if not subplots:
        plt.tight_layout()
        plt.show()


def subplot_numeric_distribution_with_feature(
    df: pd.DataFrame, categorical_feature: str, numeric_feature: str, bins: int = 20, xlim: tuple = None
) -> None:
    """
    Create subplots to visualize the relationship between two categorical features.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        categorical_feature (str): The primary categorical feature.
        numeric_feature (str): The secondary categorical feature.
        y_col (str): The column for the y-axis.
        xlim (tuple): The limits for the x-axis (optional). Format: (min, max)

    Returns:
        None
    """

    g = sns.FacetGrid(df, col=categorical_feature, col_wrap=3, height=4, sharey=True)

    g.map_dataframe(plot_numeric_distribution, feature=numeric_feature, subplots=True, xlim=xlim, bins=bins)
    g.set_titles("{col_name}")
    g.set_axis_labels(numeric_feature.replace("_", " ").title())
    g.set_xticklabels(rotation=0)
    g.set(yticks=[])
    
    plt.tight_layout()
    plt.show()


def plot_two_numeric_distributions(
    resample_means_gate_30_1: np.ndarray, 
    resample_means_gate_40_1: np.ndarray, 
    bins: int = 50, 
    color_gate_30: str = 'royalblue', 
    color_gate_40: str = 'darkorange',
    title: str = 'Bootstrap Resample Means for Gate 30 and Gate 40',
    x_axis_name: str = 'Retention Rate',
    labels: tuple = None
) -> None:
    """
    Plots the bootstrap distribution for Gate 30 and Gate 40 resample means.

    Parameters:
    - resample_means_gate_30_1: Array of bootstrap resample means for Gate 30.
    - resample_means_gate_40_1: Array of bootstrap resample means for Gate 40.
    - bins: Number of bins for the histogram (default is 50).
    - color_gate_30: Color for Gate 30's plot (default is 'royalblue').
    - color_gate_40: Color for Gate 40's plot (default is 'darkorange').
    - title: The title of the plot (default is 'Bootstrap Resample Means for Gate 30 and Gate 40').
    - x_axis_name: The name for the x-axis (default is 'Retention Rate').
    - labels: labels for distributions.


    Returns:
    - None
    """
    
    plt.figure(figsize=(10, 6))
    
    sns.histplot(resample_means_gate_30_1, kde=True, bins=bins, color=color_gate_30, label=labels[0], edgecolor="black")
    sns.histplot(resample_means_gate_40_1, kde=True, bins=bins, color=color_gate_40, label=labels[1], edgecolor="black")
    plt.title(title, fontsize=16)
    plt.xlabel(x_axis_name, fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.legend(title='')
    
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.show()




def plot_box(df: pd.DataFrame, col: str, xlim: tuple = None) -> None:
    """
    Create a boxplot to visualize outliers in a specified column of a DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        col (str): The column name to visualize outliers.
        xlim (tuple): The limits for the x-axis (optional). Format: (min, max)

    Returns:
        None
    """
    plt.figure(figsize=(12, 2))

    sns.boxplot(x=df[col], color="skyblue", width=0.5)

    sns.despine(left=True)
    plt.gca().get_yaxis().set_ticks([])

    if xlim:
        plt.xlim(xlim)

    plt.title(f"Outliers", fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_barchart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    vertical: bool = True,
    subplots: bool = False,
    show_values: bool = False,
    color: str = "#3174A1",
) -> None:
    """
    Create a bar chart for a given DataFrame.

    Parameters:
        data (pd.DataFrame): The input DataFrame.
        x_col (str): The column for the x-axis.
        y_col (str): The column for the y-axis.
        vertical (bool, optional): Whether the bars are vertical. Defaults to True.
        subplots (bool, optional): Whether to create subplots. Defaults to False.
        show_values (bool, optional): Whether to display values on bars. Defaults to False.
        color (str, optional): Color for the bars. Defaults to '#3174A1'.

    Returns:
        None
    """
    x, y = (x_col, y_col) if vertical else (y_col, x_col)

    ax = sns.barplot(data=data, x=x, y=y, edgecolor="black", color=color)

    if show_values:
        if vertical:
            for p in ax.patches:
                height = p.get_height()
                if not pd.isna(height):
                    ax.text(
                        p.get_x() + p.get_width() / 2,
                        height + 0.5,
                        f"{height:.0f}%" if y == "percentage" else int(height),
                        ha="center",
                        va="bottom",
                        fontsize=9,
                    )
        else:
            for p in ax.patches:
                height = p.get_height()
                width = p.get_width()
                y = p.get_y()
                if not pd.isna(width):
                    ax.text(width * 1.05, y + height * 0.8, f"{width:.3f}", fontsize=9)

    plt.title(f"{x_col.replace('_', ' ').title()} Distribution")
    plt.xlabel("Count")
    plt.ylabel("")

    for spine_name, spine in ax.spines.items():
        if spine_name != "bottom":
            spine.set_visible(False)

    ax.grid(axis="y", visible=False)

    if not subplots:
        plt.tight_layout()
        plt.show()


def plot_box_with_category(
    df: pd.DataFrame, numeric_feature: str, feature: str, ylim: tuple = None
) -> None:
    """
    Create a boxplot of a numeric feature grouped by a categorical feature.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        numeric_feature (str): The numeric feature to visualize.
        feature (str): The categorical feature to group by.
        ylim (tuple): The limits for the y-axis (optional). Format: (min, max)

    Returns:
        None
    """

    plt.figure(figsize=(8, 6))

    sns.boxplot(x=feature, y=numeric_feature, data=df)
    sns.despine(left=True)

    plt.title(f"Boxplot of Age by {feature.replace('_', ' ').title()}", fontsize=14)
    plt.xlabel(feature.replace("_", " ").title(), fontsize=12)
    plt.ylabel(numeric_feature.title(), fontsize=12)

    if ylim:
        plt.ylim(ylim)

    plt.tight_layout()
    plt.show()


def encode_feature_from_list(df: pd.DataFrame, encode_feature: str) -> pd.DataFrame:
    """
    Encode a feature containing lists into separate binary columns.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        encode_feature (str): The feature containing lists to encode.

    Returns:
        pd.DataFrame: The updated DataFrame with encoded columns.
    """

    mlb = MultiLabelBinarizer()
    df[encode_feature] = df[encode_feature].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    encoded_data = mlb.fit_transform(df[encode_feature])
    role_df = pd.DataFrame(encoded_data, columns=mlb.classes_)
    role_df = role_df.add_prefix(f"{encode_feature}_")
    df = pd.concat([df, role_df], axis=1)
    df = df.drop(columns=[encode_feature])
    return df


def count_group_total_percentage(
    df: pd.DataFrame, feature_1: str, feature_2: str
) -> pd.DataFrame:
    """
    Calculate the count, total, and percentage for grouped categories in a DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        feature_1 (str): The primary grouping feature.
        feature_2 (str): The secondary grouping feature.

    Returns:
        pd.DataFrame: A DataFrame with counts, totals, and percentages.
    """

    count_data = (
        df.groupby([feature_1, feature_2], observed=False)
        .size()
        .reset_index(name="count")
    )
    count_data_with_totals = count_data.merge(
        count_data.groupby(feature_1, observed=False)["count"]
        .sum()
        .reset_index(name="total"),
        on=feature_1,
        how="left",
    )
    count_data_with_totals["percentage"] = round(
        (count_data_with_totals["count"] / count_data_with_totals["total"]) * 100, 1
    )
    return count_data_with_totals


def subplot_two_categorical_distribution(
    df: pd.DataFrame, feature_1: str, feature_2: str
) -> None:
    """
    Plot side-by-side distributions of two categorical features.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        feature_1 (str): The first categorical feature.
        feature_2 (str): The second categorical feature.

    Returns:
        None
    """

    plt.figure(figsize=(16, 4))

    plt.subplot(1, 2, 1)
    plot_categorical_distribution(df, feature_1, show=False)

    plt.subplot(1, 2, 2)
    plot_categorical_distribution(df, feature_2, show=False)

    plt.tight_layout()
    plt.show()


def subplot_two_categorical_features(
    df: pd.DataFrame, feature_1: str, feature_2: str, y_col: str
) -> None:
    """
    Create subplots to visualize the relationship between two categorical features.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        feature_1 (str): The primary categorical feature.
        feature_2 (str): The secondary categorical feature.
        y_col (str): The column for the y-axis.

    Returns:
        None
    """

    g = sns.FacetGrid(df, col=feature_1, col_wrap=7, height=4, sharey=True)

    g.map_dataframe(
        plot_barchart, x_col=feature_2, y_col=y_col, subplots=True, show_values=True
    )

    g.set_titles("{col_name}")
    g.set_axis_labels(feature_2.replace("_", " ").title())
    g.set_xticklabels(rotation=0)
    g.set(yticks=[])

    plt.show()


def create_world_map(data_dict: dict) -> folium.Map:
    """
    Create a world map with country-level data distribution.

    Parameters:
        data_dict (dict): Dictionary containing country data.

    Returns:
        folium.Map: The generated world map.
    """

    with open(".\\data\\geo.json", "r") as f:
        geo_data = json.load(f)

    m = folium.Map(location=[20, 0], zoom_start=3)

    folium.Choropleth(
        geo_data=geo_data,
        name="choropleth",
        data=data_dict,
        columns=["Country", "Value"],
        key_on="feature.properties.name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Country Distribution",
    ).add_to(m)

    folium.GeoJson(
        geo_data,
        style_function=lambda x: {"fillOpacity": 0, "weight": 1, "color": "black"},
    ).add_to(m)

    def add_numbers_to_map(geo_data, distribution_data):
        for feature in geo_data["features"]:
            country_name = feature["properties"]["name"]

            if country_name in distribution_data:
                geometry = shape(feature["geometry"])

                centroid = geometry.centroid

                lat, lon = centroid.y, centroid.x

                folium.Marker(
                    location=[lat, lon],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 10pt; color: black;">{distribution_data[country_name]}</div>'
                    ),
                ).add_to(m)

    add_numbers_to_map(geo_data, data_dict)

    m.save(".\\data\\country_distribution_with_numbers_and_borders.html")
    return m


def create_us_map(state_dict: dict, state_dict_percentage: dict) -> folium.Map:
    """
    Create a US map with state-level data and percentages.

    Parameters:
        state_dict (dict): Dictionary containing state data.
        state_dict_percentage (dict): Dictionary containing state percentages.

    Returns:
        folium.Map: The generated US map.
    """

    with open(".\\data\\geo_us-states.json", "r") as f:
        geo_data = json.load(f)

    latitude = 36.7783
    longitude = -97

    m = folium.Map(location=[latitude, longitude], zoom_start=4.5)

    folium.Choropleth(
        geo_data=geo_data,
        name="choropleth",
        data=state_dict,
        columns=["US states", "Value"],
        key_on="feature.properties.name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="US states Distribution",
    ).add_to(m)

    folium.GeoJson(
        geo_data,
        style_function=lambda x: {"fillOpacity": 0, "weight": 1, "color": "black"},
    ).add_to(m)

    def add_numbers_to_map(geo_data, distribution_data, distribution_percentage):
        for feature in geo_data["features"]:
            state_name = feature["properties"]["name"]

            if state_name in distribution_data:
                geometry = shape(feature["geometry"])

                centroid = geometry.centroid

                lat, lon = centroid.y, centroid.x - 1

                folium.Marker(
                    location=[lat, lon],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 10pt; color: black;">{distribution_data[state_name]}&nbsp;({distribution_percentage[state_name]}%)</div>'
                    ),
                ).add_to(m)

    add_numbers_to_map(geo_data, state_dict, state_dict_percentage)

    m.save(".\\data\\country_distribution_with_numbers_and_borders.html")

    return m


def cramers_v(x: pd.Series, y: pd.Series) -> float:
    """
    Calculate Cramér's V statistic for categorical-categorical association.

    Parameters:
        x (pd.Series): First categorical variable.
        y (pd.Series): Second categorical variable.

    Returns:
        float: The Cramér's V statistic.
    """

    contingency_table = pd.crosstab(x, y)
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    r, k = contingency_table.shape
    return np.sqrt(chi2 / (n * (min(r, k) - 1)))


def categorical_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a correlation matrix for categorical features.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with correlation values.
    """

    categorical_columns = df.select_dtypes(include=["object", "category"]).columns
    n = len(categorical_columns)
    corr_matrix = pd.DataFrame(
        np.zeros((n, n)), index=categorical_columns, columns=categorical_columns
    )

    for i, col1 in enumerate(categorical_columns):
        for j, col2 in enumerate(categorical_columns):
            if i != j:
                corr_matrix.iloc[i, j] = cramers_v(df[col1], df[col2])
            else:
                corr_matrix.iloc[i, j] = 1

    return corr_matrix


def plot_heatmap(
    corr_matrix: pd.DataFrame,
    linewidths: int = 0,
    figsize: tuple = (10, 8),
    fmt: str = ".2f",
    title: str = "",
    mask_upper: bool = True  # New parameter to choose which side to mask
) -> None:
    """
    Plot a heatmap for a given correlation matrix with an option to mask one half.

    Parameters:
        corr_matrix (pd.DataFrame): The correlation matrix.
        linewidths (int, optional): Line width for the heatmap. Defaults to 0.
        figsize (tuple, optional): Figure size. Defaults to (10, 8).
        fmt (str, optional): Format for annotation text. Defaults to ".2f".
        title (str, optional): Title for the plot. Defaults to "".
        mask_upper (bool, optional): Whether to mask the upper triangle. Defaults to True.

    Returns:
        None
    """
    mask = np.zeros_like(corr_matrix, dtype=bool)
    if mask_upper:
        mask[np.triu_indices_from(mask)] = True  # Mask the upper triangle
    else:
        mask[np.tril_indices_from(mask)] = True  # Mask the lower triangle

    plt.figure(figsize=figsize)
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=fmt,
        linewidths=linewidths,
        mask=mask
    )
    plt.title(title)
    plt.show()








def categorical_and_numeric_correlation(
    df: pd.DataFrame, numeric_feature: str, categorical_columns: list
) -> pd.DataFrame:
    """
    Compute ANOVA p-values for numeric-categorical feature pairs.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        numeric_feature (str): The numeric feature.
        categorical_columns (list): List of categorical features.

    Returns:
        pd.DataFrame: A DataFrame with p-values for each categorical feature.
    """

    p_values = {}
    for col in categorical_columns:
        groups = [
            df[df[col] == category][numeric_feature] for category in df[col].unique()
        ]
        f_stat, p_value = stats.f_oneway(*groups)
        p_values[col] = p_value

    p_values_df = pd.DataFrame(list(p_values.items()), columns=["Feature", "p_value"])

    return p_values_df.set_index("Feature")


def encode_categorical_features(
    df: pd.DataFrame, categorical_features: list
) -> pd.DataFrame:
    """
    One-hot encode categorical features in a DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        categorical_features (list): List of categorical features to encode.

    Returns:
        pd.DataFrame: The updated DataFrame with one-hot encoded features.
    """

    encoder = OneHotEncoder(drop="first", sparse_output=False)

    encoded_array = encoder.fit_transform(df[categorical_features])

    encoded_df = pd.DataFrame(
        encoded_array, columns=encoder.get_feature_names_out(categorical_features)
    )

    df_joined = pd.concat([df, encoded_df], axis=1)

    df_joined = df_joined.drop(columns=categorical_features)

    return df_joined


def count_prevalence_rate(df: pd.DataFrame, conditions: list) -> pd.DataFrame:
    """
    Calculate prevalence rates and confidence intervals for conditions.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        conditions (list): List of conditions to analyze.

    Returns:
        pd.DataFrame: A DataFrame with prevalence rates and confidence intervals.
    """

    prevalence_rates = []
    lower_bounds = []
    upper_bounds = []
    for condition in conditions:
        prevalence = df[condition].mean()

        positive_count = df[condition].sum()
        all_count = len(df)
        lower, upper = proportion_confint(
            positive_count, all_count, alpha=0.05, method="wilson"
        )

        prevalence_rates.append(prevalence)
        lower_bounds.append(lower)
        upper_bounds.append(upper)

    prevalence_df = pd.DataFrame(
        {
            "Condition": conditions,
            "Prevalence Rate": prevalence_rates,
            "Lower Bound": lower_bounds,
            "Upper Bound": upper_bounds,
        }
    )

    return prevalence_df


def plot_prevalence_rate(df: pd.DataFrame) -> None:
    """
    Plot prevalence rates with confidence intervals for conditions.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        None
    """

    sns.barplot(
        x="Prevalence Rate", y="Condition", data=df, edgecolor="black", color="#3174A1"
    )

    for i in range(len(df)):
        plt.plot(
            [df["Lower Bound"][i], df["Upper Bound"][i]], [i, i], color="black", lw=1
        )

        plt.plot(
            [df["Lower Bound"][i], df["Lower Bound"][i]],
            [i - 0.2, i + 0.2],
            color="black",
            lw=1,
        )
        plt.plot(
            [df["Upper Bound"][i], df["Upper Bound"][i]],
            [i - 0.2, i + 0.2],
            color="black",
            lw=1,
        )

    plt.title(
        "Prevalence Rates of Mental Health Conditions with 95% Confidence Intervals"
    )
    plt.xlabel("Prevalence Rate")
    plt.ylabel("Condition")
    plt.xlim(0, 1)
    plt.show()



def create_scatter_chart(df: pd.DataFrame, x: str, y: str) -> None:
    """
    Create a scatter plot to visualize the relationship between two features.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        x (str): The feature for the x-axis.
        y (str): The feature for the y-axis.

    Returns:
        None
    """
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x=x, y=y, alpha=0.7)

    plt.title(f"{x.replace('_', ' ').title()} vs {y.replace('_', ' ').title()}", fontsize=16)
    plt.xlabel(x.replace('_', ' ').title(), fontsize=12)
    plt.ylabel(y.replace('_', ' ').title(), fontsize=12)

    sns.despine()
    plt.tight_layout()
    plt.show()


