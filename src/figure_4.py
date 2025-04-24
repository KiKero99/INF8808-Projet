import plotly.graph_objects as go
from const import INJURY_CATEGORIES, INJURY_LABEL_MAPPING, COLORS_MAP_FIG_4

def generate_sunburst_figure_4(data):
    """
    Generates a Sunburst chart visualizing the distribution of accident injuries and their causes.

    Args:
        data (pd.DataFrame): The dataframe to display.

    Returns:
        go.Figure: A Plotly figure containing a Sunburst chart showing injury categories 
                   and their corresponding cause categories.
    """
    labels = ["Total"]
    parents = [""]
    values = [data["count"].sum()]

    for inj in INJURY_CATEGORIES:
        mapped_inj = INJURY_LABEL_MAPPING.get(inj, inj.replace("_", " "))
        inj_sum = data[data["injury_category"] == inj]["count"].sum()
        labels.append(mapped_inj)
        parents.append("Total")
        values.append(inj_sum)

        for _, row in data[data["injury_category"] == inj].iterrows():
            labels.append(row["cause_category"])
            parents.append(mapped_inj)
            values.append(row["count"])

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        textfont=dict(size=17),
        marker=dict(
            colors=[COLORS_MAP_FIG_4.get(label, "#bdc3c7") for label in labels],
            line=dict(color='black', width=1)
        )
    ))

    fig.update_layout(
        title={
            'text': "<b>Blessures et causes d'accidents</b>",
            'x': 0.5,
            'xanchor': "center",
            'yanchor': 'top',
        },
        height=650,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    return fig

def generate_sankey_figure_4(data):
    """
    Generates a Sankey diagram visualizing the distribution of injuries and their corresponding causes.

    Args:
        data (pd.DataFrame): The dataframe to display.

    Returns:
        go.Figure: A Plotly figure containing a Sankey diagram that illustrates the flow from total injuries
                   to injury categories and their associated causes.
    """
    node_labels = ["Total"]
    injury_nodes = [INJURY_LABEL_MAPPING[i] for i in INJURY_CATEGORIES]
    cause_nodes = list(data["cause_category"].unique())

    node_labels.extend(injury_nodes)
    node_labels.extend([c for c in cause_nodes])

    label_to_index = {label: idx for idx, label in enumerate(node_labels)}

    sources = []
    targets = []
    values = []

    for inj in INJURY_CATEGORIES:
        inj_label = INJURY_LABEL_MAPPING[inj]
        inj_total = data[data["injury_category"] == inj]["count"].sum()

        sources.append(label_to_index["Total"])
        targets.append(label_to_index[inj_label])
        values.append(inj_total)

        for _, row in data[data["injury_category"] == inj].iterrows():
            sources.append(label_to_index[inj_label])
            targets.append(label_to_index[row["cause_category"]])
            values.append(row["count"])

    node_colors = [COLORS_MAP_FIG_4.get(label, "#cccccc") for label in node_labels]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            label=node_labels,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(169, 169, 169, 0.6)",
            line=dict(color="rgba(169, 169, 169, 0.6)", width=2)
        )
    ))

    fig.update_layout(
        title={
            'text': "<b>Blessures et causes d'accidents</b>",
            'x': 0.5,
            'xanchor': "center",
            'yanchor': 'top',
        },
        height=600,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )

    return fig
