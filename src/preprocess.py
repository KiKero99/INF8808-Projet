import pandas as pd
from categories_const import CAUSE_MAP, WEATHER_MAP, TRAFFIC_MAP
from const import INJURY_CATEGORIES


def convert_types(df):
    """
    Converts specific columns in the DataFrame to appropriate data types and extracts 
    additional date-related features from the 'crash_date' column.

    Args:
        df (pd.DataFrame): Base Dataframe.

    Returns:
        pd.DataFrame: Dtaframe with updated types.
    """
    df['crash_date'] = pd.to_datetime(df['crash_date'])
    df['crash_year'] = df['crash_date'].dt.year
    df['crash_day_of_week'] = df['crash_date'].dt.dayofweek
    df['crash_day_of_week_name'] = df['crash_date'].dt.day_name()
    df['crash_month_name'] = df['crash_date'].dt.month_name()  
    return df

def map_categories(df):
    """
    Maps and categorizes the 'prim_contributory_cause', 'weather_condition', and 'trafficway_type' columns 
    into separate categories using the 'categorize_all' function.

    Args:
        df (pd.DataFrame): Base Dataframe

    Returns:
        pd.DataFrame: The updated DataFrame with updated colums for the categories.
    """
    df[["cause_category", "weather_category", "trafficway_category"]] = df.apply(
    lambda row: categorize_all(
        row["prim_contributory_cause"],
        row["weather_condition"],
        row["trafficway_type"]
    ),
    axis=1,
    result_type='expand'
    )

    return df


def categorize_all(cause, weather, traffic):
    """
    Categorizes the given cause, weather, and traffic conditions by mapping them to predefined categories 
    using their respective maps.

    Args:
        cause (str): The primary contributory cause of the accident.
        weather (str): The weather condition during the accident.
        traffic (str): The traffic type at the time of the accident.

    Returns:
        Tuple[str, str, str]: A tuple containing the categorized values for cause, weather, and traffic.
    """
    return (
        get_category(cause, CAUSE_MAP),
        get_category(weather, WEATHER_MAP),
        get_category(traffic, TRAFFIC_MAP)
    )


def get_category(value, mapping):
    """
    Retrieves the category for a given value based on a predefined mapping.

    Args:
        value (str): The value to be categorized.
        mapping (Dict[str, list]): A dictionary where the keys are category names 
                                   and the values are lists of possible values for each category.

    Returns:
        str: The category corresponding to the given value, or 'Autre' if no match is found.
    """
    for cat, values in mapping.items():
        if value in values:
            return cat
    return "Autre"
    
def add_season(df) :
    """
    Adds a 'season' column to the DataFrame based on the 'crash_month_name' column.

    Args:
        df (pd.DataFrame): A DataFrame to update.

    Returns:
        pd.DataFrame: The updated DataFrame with a new 'season' column indicating the season of each crash.
    """
    season_mapping = {
        'December': 'Hiver', 'January': 'Hiver', 'February': 'Hiver',
        'March': 'Printemps', 'April': 'Printemps', 'May': 'Printemps',
        'June': 'Été', 'July': 'Été', 'August': 'Été',
        'September': 'Automne', 'October': 'Automne', 'November': 'Automne'
    }

    df['season'] = df['crash_month_name'].map(season_mapping)
    return df

def prepare_seasonal_accidents(df) :
    """
    Prepares a DataFrame of seasonal accidents by grouping data by 'crash_year' and 'season',
    and counting the number of accidents for each combination.

    Args:
        df (pd.DataFrame): A DataFrame to update.

    Returns:
        pd.DataFrame: A DataFrame where each row corresponds to a year and each column represents
                      a season, with the number of accidents in each season.
    """
    seasonal_accidents = df.groupby(['crash_year', 'season']).size().unstack().fillna(0)
    return seasonal_accidents

def prepare_figure_4(df) : 
    """
    Prepares aggregated data for figure 4 by filtering out 'Autre' cause categories,
    then summing the counts for each injury category and cause category.

    Args:
        df (pd.DataFrame): A DataFrame to update.

    Returns:
        pd.DataFrame: A DataFrame to display.
    """
    df_filtered = df[df["cause_category"] != 'Autre']
    agg_data = pd.DataFrame(columns=["injury_category", "cause_category", "count"])
    for injury in INJURY_CATEGORIES:
        temp_data = df_filtered.groupby("cause_category")[injury].sum().reset_index(name="count")
        temp_data["injury_category"] = injury
        agg_data = pd.concat([agg_data, temp_data], ignore_index=True)

    return agg_data
    