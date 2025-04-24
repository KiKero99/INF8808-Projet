import plotly.graph_objects as go
from plotly.subplots import make_subplots


from const import DAY_ORDER, DAY_LABELS

color = "rgba(30,144,255,0.5)" 

def draw(data, selected_days = DAY_ORDER) :
    """
    Draws a radar chart showing the hourly distribution of accidents for selected days of the week.

    Args:
        data (pd.DataFrame): The dataframe to display.
        selected_days (list[str], optional): List of days to include in the radar chart. Defaults to DAY_ORDER.

    Returns:
        go.Figure: A Plotly figure containing radar charts (subplots) for each selected day,
                   displaying hourly accident distributions.
    """
    all_hours = list(range(24))
    categories = [str(h) for h in all_hours]
    day_names = [day for day in DAY_ORDER if day in selected_days and day in data['crash_day_of_week_name'].unique()]

    fig = make_subplots(
        rows=2, cols=4,
        specs=[[{'type': 'polar'}]*4, [{'type': 'polar'}]*4],
        subplot_titles=[ 
            f"{DAY_LABELS[day]}<br>Total: {data[data['crash_day_of_week_name'] == day].shape[0]} accidents"
            for day in day_names
        ] + [""],
        vertical_spacing=0.08, 
        horizontal_spacing=0.08 
    )

    fig.update_layout(
        title={
            'text': '<b>Accidents par heure selon le jour de la semaine</b>',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'y': 0.97,
        },
        height=800,
        showlegend=False,
        plot_bgcolor='rgba(0, 0, 0, 0)',  
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(t=120, b=50),
    )

    for i, day_name in enumerate(day_names):
        df_day = data[data['crash_day_of_week_name'] == day_name]
        day_counts = df_day.groupby('crash_hour').size().reindex(all_hours, fill_value=0)
        day_values = list(day_counts) + [day_counts.iloc[0]]  # Close loop

        r = day_values
        theta = categories + [categories[0]]

        row = i // 4 + 1
        col = i % 4 + 1

        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=theta,
            fill='toself',
            mode='lines+markers',
            text=[f"{DAY_LABELS[day_name]}<br>{h}h : {v} accidents" for h, v in zip(theta, r)],
            hovertemplate="%{text}<extra></extra>",
            line=dict(color="black", width=1),
            marker=dict(size=4, opacity=0),
            fillcolor=color,
        ), row=row, col=col)

    fig.update_polars(
        angularaxis=dict(
            direction="clockwise",
            rotation=90,
            tickmode='array',
            tickvals=[str(h) for h in range(0, 24)],
            ticktext=[f"{h}h" for h in range(0, 24)],
        ),
        radialaxis=dict(showticklabels=False),
    )

    for annotation in fig['layout']['annotations']:
        annotation['yshift'] = 1  

    return fig
