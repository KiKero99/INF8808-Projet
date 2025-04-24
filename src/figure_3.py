import plotly.graph_objects as go

from const import COLOR_MAP

def process_data(data):
    """
    Processes the input data to generate categories and link data for a Sankey diagram, based on cause, weather, and trafficway categories.

    Args:
        data (pd.DataFrame): The dataframe to display.

    Returns:
        tuple: A tuple containing:
            - The processed DataFrame with counts ('cause_category', 'weather_category', 'trafficway_category', 'count').
            - A list of unique categories combining cause, weather, and trafficway categories.
            - A list of sources.
            - A list of targets.
            - A list of values.
    """
    data = data.groupby(["cause_category", "weather_category", "trafficway_category"]).size().reset_index(name="count")
    
    categories = list(set(data["cause_category"]) | set(data["weather_category"]) | set(data["trafficway_category"]))
    label_to_index = {label: i for i, label in enumerate(categories)}
    
    links_cause_weather = data.groupby(["cause_category", "weather_category"])["count"].sum().reset_index()
    source1 = [label_to_index[row["cause_category"]] for _, row in links_cause_weather.iterrows()]
    target1 = [label_to_index[row["weather_category"]] for _, row in links_cause_weather.iterrows()]
    value1 = links_cause_weather["count"].tolist()

    links_weather_traffic = data.groupby(["weather_category", "trafficway_category"])["count"].sum().reset_index()
    source2 = [label_to_index[row["weather_category"]] for _, row in links_weather_traffic.iterrows()]
    target2 = [label_to_index[row["trafficway_category"]] for _, row in links_weather_traffic.iterrows()]
    value2 = links_weather_traffic["count"].tolist()

    source = source1 + source2
    target = target1 + target2
    value = value1 + value2

    return data, categories, source, target, value

def get_node_colors(labels):
    """
    Returns a list of colors for the given labels, using a predefined color map. 
    If a label is not found in the color map, a default color is used.

    Args:
        labels (List[str]): A list of labels for which colors are required.

    Returns:
        List[str]: A list of color codes corresponding to the labels.
    """
    default_color = "#bdc3c7"
    return [COLOR_MAP.get(label, default_color) for label in labels]

def draw(data):
    """
    Draws a Sankey diagram visualizing the relationship between accident causes, weather conditions, 
    and trafficway categories based on the provided data.

    Args:
        data (pd.DataFrame): The dataframe to display.

    Returns:
        go.Figure: A Plotly figure containing a Sankey diagram with nodes representing the categories
                   and links representing the relationships between them.
    """
    data, categories, source, target, value = process_data(data)
    node_colors = get_node_colors(categories)
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=categories,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color="rgba(0,0,0,0.2)"
        )
    ))

    fig.update_layout(
        title=dict(
            text="<b>Analyse croisée des causes d’accidents selon la météo et les routes</b>",
            x=0.5, xanchor="center", yanchor="top", y=0.97
        ),
        font=dict(size=12),
        height=550,
        margin=dict(t=120, b=50),
        hovermode="x",
        showlegend=False,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    return fig
