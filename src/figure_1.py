import plotly.graph_objects as go

from const import SEASON_COLORS, SEASON_ORDER

def init_figure():
    """
    Initializes a Plotly figure with a predefined layout for a stacked bar chart 
    displaying the number of accidents per year.

    Returns:
        go.Figure: A configured Plotly figure ready to receive data traces.
    """
    fig = go.Figure()
    fig.update_layout(
        barmode='stack',
        xaxis_title="Nombre d'accidents",
        yaxis_title="Année",
        legend_title='Saison',
        showlegend=False,
        plot_bgcolor='rgba(0, 0, 0, 0)',  
        paper_bgcolor='rgba(0, 0, 0, 0)',
        yaxis=
        dict(
            tickmode='linear',
            dtick=1,
            type='linear',
            autorange='reversed'
        ),
        margin=dict(l=60, r=20, t=40, b=60)
    )
    return fig

def draw(fig, data, year_start = 2018, year_end = 2024, selected_seasons = SEASON_ORDER) :
    """
    Draws a stacked horizontal bar chart into the given Plotly figure, based on accident data
    filtered by year range and selected seasons.

    Args:
        fig (go.Figure): The base figure to update.
        data (pd.DataFrame): The dataframe to display.
        year_start (int, optional): Start year for filtering the data. Defaults to 2018.
        year_end (int, optional): End year for filtering the data. Defaults to 2024.
        selected_seasons (list[str], optional): List of seasons to include in the chart. Defaults to SEASON_ORDER.

    Returns:
        go.Figure: The updated Plotly figure containing the bar traces.
    """
    fig = go.Figure(fig)
    fig.data = []
    seasons_to_show = [season for season in SEASON_ORDER if season in selected_seasons]
    data_filtered = data.loc[data.index.to_series().between(year_start, year_end)]   
    year_totals = data_filtered.sum(axis=1).to_dict()
    years = list(range(year_start, year_end + 1))

    for season in seasons_to_show:
        values = [data_filtered.loc[year, season] if season in data_filtered.columns else 0 for year in years]
        hover_texts = [
        f"{season} – {int(v)} accidents<br>Total en {year} : {year_totals.get(year, 0)}"
        if v > 0 else ''
        for v, year in zip(values, years)
        ]
        fig.add_trace(go.Bar(
            y=years,
            x=values,
            name=season,
            marker_color=SEASON_COLORS[season],
            orientation='h',
            text=[str(int(v)) if v > 0 else '' for v in values],
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=12),
            hoverinfo='text',
            hovertext=hover_texts
        ))
    return fig