import dash
import pathlib
import preprocess
import figure_1
import figure_2
import figure_3
import figure_4
from dash import ctx
from dash import html
from dash.dependencies import Input, Output, State
from dash import dcc

import plotly.graph_objects as go

import pandas as pd
from const import SEASON_ORDER, SEASON_COLORS

app = dash.Dash(__name__)
app.title = 'La face cachée de nos trajets quotidiens'
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

def load_data() :
    """
    Loads the traffic accident data from a CSV file, processes it, and returns the cleaned DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the processed traffic accident data.
    """
    df = pd.read_csv(DATA_PATH.joinpath("traffic_accidents.csv"))
    data = preprocess.convert_types(df)
    data = preprocess.add_season(data)
    data = preprocess.map_categories(data)
    return data

def prep_data(data) :
    """
    Prepares data for different figures by processing and aggregating it.

    Args:
        data (pd.DataFrame): A DataFrame containing the processed traffic accident data.

    Returns:
        tuple: A tuple containing four DataFrames:
               - `data_fig_1`: data for fig 1.
               - `data`: data for fig 2.
               - `data`: data for fig 3.
               - `data_fig_4`: data for fig 4.
    """
    data_fig_1 = preprocess.prepare_seasonal_accidents(data)
    data_fig_4 = preprocess.prepare_figure_4(data)
    return data_fig_1, data, data, data_fig_4

def init_figure(data_fig_1, data_fig_2, data_fig_3, data_fig_4):
    """
    Initializes and generates multiple figures (1 to 4) using provided data for each figure.

    Args:
        data_fig_1 (pd.DataFrame): Data for figure 1.
        data_fig_2 (pd.DataFrame): Data for figure 2.
        data_fig_3 (pd.DataFrame): Data for figure 3.
        data_fig_4 (pd.DataFrame): Data for figure 4.

    Returns:
        tuple: A tuple containing five Plotly figures:
               - `figure1`: A bar plot (figure 1).
               - `figure2`: A radar chart (figure 2).
               - `figure3`: A Sankey diagram (figure 3).
               - `figure4`: A sunburst chart (figure 4).
               - `figure4_alt`: A Sankey diagram (alternative representation for figure 4).
    """
    figure1 = figure_1.init_figure()
    figure1 = figure_1.draw(figure1, data_fig_1)

    figure2 = figure_2.draw(data_fig_2)

    figure3 = figure_3.draw(data_fig_3)

    figure4 = figure_4.generate_sunburst_figure_4(data_fig_4)
    figure4_alt = figure_4.generate_sankey_figure_4(data_fig_4)
    return figure1, figure2, figure3, figure4, figure4_alt


def init_app_layout(figure1, figure2, figure3):
    """
    Initializes the layout for the app with various sections and interactive html components.

    Args:
        figure1 (Figure): The first Plotly figure, bar plot.
        figure2 (Figure): The second Plotly figure, radar chart.
        figure3 (Figure): The third Plotly figure, sankey diagram.

    Returns:
        html.Div: The layout of the app as a HTML Div component, containing multiple sections
                  for each graph.
    """
    return html.Div(className="page", children=[
        html.Div(className="top-bar",
                 children=[
                     html.Div(className="left", children="INF8808"),
                     html.Div(className="center",children="PolyInfo"),
                     html.Img(className="right",src="/assets/logo.png", alt="Logo"),
                 ]),
        html.Div(
            className="main-content",
            children=[
                html.Div(
                    className="content-wrapper",
                    children=[
                        html.Div(
                            className="page-header",
                            children=[
                                html.H3("Quand la routine dérape", className="main-title"),
                                html.P(
                                    "Une immersion interactive dans les dessous des accidents de la route. "
                                    "Explorez les données, comprenez les tendances, et découvrez les histoires que les chiffres racontent.",
                                    className="page-description"
                                )
                            ]
                        ),

                        html.Section(id="section1", className="content-section", children=[
                            html.H3("Une menace invisible mais constante"),
                            html.P("Chaque année, des milliers d’accidents surviennent. La première visualisation présente cette évolution annuelle, découpée par saison.", className="paragraph-style"),
                            dcc.RangeSlider(
                                id='year-slider',
                                min=2018,
                                max=2024,
                                step=1,
                                count=1,
                                marks={year: str(year) for year in range(2018, 2025)},
                                value=[2018, 2024],
                                allowCross=False,
                                tooltip={"placement": "bottom", "always_visible": True},
                                className='slider-style'
                            ), 
                            html.Div(className="title-season", id="dynamic-title"),  
                            html.Div(style={'display': 'flex', 'gap': '20px', 'alignItems': 'center', 'flexWrap': 'wrap'}, children=[
                                html.Div(style={'flex': '1'}, children=[
                                    dcc.Graph(id='figure1', figure=figure1, config={'staticPlot': False})
                                ]),
                                html.Div(style={'minWidth': '200px'}, children=[
                                    html.Div("Sélectionner des saisons particulières", className="button-selector"),
                                    html.Div(className="button-container", style={'flexDirection': 'column', 'alignItems': 'stretch'}, children=[
                                        html.Button(f"{season}", className="button-season selected", id=f"button-{season}", style={'backgroundColor': SEASON_COLORS[season], 'width': '100%'}) for season in SEASON_ORDER
                                    ])
                                ])
                            ]), 
                            html.P(
                                "Entre 2018 et 2024, le nombre total d’accidents de la route reste étonnamment stable d’une année à l’autre, se situant autour des 25 000 cas. Mais derrière cette régularité apparente, les saisons racontent une autre histoire. En 2020, la pandémie de COVID-19 a provoqué une chute historique : au printemps, les accidents tombent à 4308, et l’été, pourtant habituellement critique, n’en compte que 6345 — un effet direct des confinements et de la réduction massive des déplacements.",
                                className="paragraph-style"
                            ),
                            html.P(
                                "Dès l’été 2021, le relâchement post-confinement provoque un effet rebond spectaculaire, avec 7242 accidents. Depuis, les saisons estivales et automnales restent les plus accidentogènes, tandis que l’hiver, chaque année, demeure la plus « calme ». La stabilité annuelle masque ainsi de fortes variations saisonnières, reflets de nos habitudes, de nos libertés retrouvées… et parfois de nos excès.",
                                className="paragraph-style"
                            ),

                        ]),
                        html.Section(id="section2", className="content-section", children=[
                            html.H3("Quand le quotidien devient risqué"),
                            html.P("Le danger est au cœur des routines. Certains moments comme les sorties de travail ou les weekends sont plus accidentogènes.", className="paragraph-style"),
                            dcc.Checklist(
                                id='day-checklist',
                                options=[
                                    {'label': 'Lundi', 'value': 'Monday'},
                                    {'label': 'Mardi', 'value': 'Tuesday'},
                                    {'label': 'Mercredi', 'value': 'Wednesday'},
                                    {'label': 'Jeudi', 'value': 'Thursday'},
                                    {'label': 'Vendredi', 'value': 'Friday'},
                                    {'label': 'Samedi', 'value': 'Saturday'},
                                    {'label': 'Dimanche', 'value': 'Sunday'},
                                ],
                                value=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],  # All selected by default
                                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                            ),        

                            dcc.DatePickerRange(
                                id='date-picker-range',
                                start_date=(data_fig_2['crash_date'].min().date()),
                                end_date=data_fig_2['crash_date'].max().date(),
                                display_format='DD/MM/YYYY', 
                                style={'margin-top': '10px', 'margin-bottom': '20px', 'display': 'block', 'textAlign': 'center'}

                            ),                    
                            dcc.Graph(
                                figure=figure2,
                                id='radar-graph',
                                config={
                                    'displayModeBar': False,  
                                    'scrollZoom': False,
                                    'staticPlot': False,
                                }
                            ),
                            html.P(
                                "C'est une réalité que peu de conducteurs réalisent au quotidien : certains moments sont bien plus accidentogènes que d'autres. En regardant de près les données d'accidents heure par heure, un schéma se dessine et il est loin d'être anodin.",
                                className="paragraph-style"
                            ),
                            html.P(
                                "En semaine, du lundi au jeudi, les journées suivent un rythme presque chorégraphique. Deux pics se détachent nettement : un premier entre 7h et 9h du matin, l'autre entre 16h et 18h. Sans surprise, ces créneaux coïncident avec les allers-retours domicile-travail, ces moments où les routes débordent de stress, de fatigue et... de distractions.",
                                className="paragraph-style"
                            ),
                            html.P(
                                "Mais le vendredi change la donne. Avec 34 458 accidents recensés, il dépasse largement les autres jours. Pourquoi ? Peut-être parce qu'on est déjà tourné vers le week-end, moins concentré, plus pressé de rentrer ou de partir. Les comportements changent, et les routes en font les frais.",
                                className="paragraph-style"
                            ),
                            html.P(
                                "Le week-end, justement, affiche un tout autre visage. Fini le rythme métro-boulot-dodo. Les pics d'accidents se déplacent, s'étalent sur la journée et prennent d'assaut la soirée. Le samedi, les accidents grimpent en fin d'après-midi et en soirée, suivant le tempo des sorties et des loisirs.",
                                className="paragraph-style"
                            ),
                            html.P(
                                "Mais c'est le dimanche à 2h du matin qui interpelle le plus : un pic inattendu, inquiétant. Un moment où la majorité dort... sauf ceux qui rentrent de soirée. Ce rebond nocturne traduit sans doute les conséquences d'un samedi soir trop arrosé ou d'un retour tardif, souvent dans des conditions loin d'être idéales.",
                                className="paragraph-style"
                            ),
                            html.P(
                                "Au final, cette plongée dans les chiffres nous rappelle une chose : chaque moment sur la route n'a pas le même niveau de risque. Et parfois, le danger se cache là où on ne l'attend pas, au cœur même de nos habitudes.",
                                className="paragraph-style"
                            ),
                        ]),

                        html.Section(id="section3", className="content-section", children=[
                            html.H3("Quand les éléments se déchaînent"),
                            html.P("Pluie, brouillard… le climat rend certaines routes plus dangereuses. Le Sankey met en lumière les combinaisons de risques.", className="paragraph-style"),
                            dcc.Graph(figure=figure3, config={'staticPlot': True}),
                            html.P(
                                "Ce diagramme de Sankey illustre les liens entre les causes d’accidents, les conditions météorologiques et les types de routes. On observe que la conduite imprudente est la cause la plus fréquente, suivie des infractions et des distractions du conducteur. De manière surprenante, la majorité des accidents se produisent par temps clair, ce qui suggère que les comportements à risque sont plus déterminants que les conditions climatiques elles-mêmes. Les intersections et routes divisées sont les lieux les plus concernés, ce qui reflète leur complexité et leur dangerosité.",
                                className="paragraph-style"
                            ),
                            html.P(
                                "Ce graphique met en évidence l’interdépendance des facteurs dans la survenue des accidents. Il souligne que les causes humaines restent dominantes, même en l’absence de conditions météorologiques défavorables. Il montre également que certains environnements (comme les routes spéciales ou en mauvais temps) présentent une vulnérabilité particulière. En résumé, ce Sankey permet de visualiser les combinaisons les plus à risque, et constitue un outil pertinent pour cibler les actions de prévention routière.",
                                className="paragraph-style"
                            ),
                        ]),

                        html.Section(id="section4", className="content-section", children=[
                            html.Div([
                                html.H3("L’impact humain"),
                                html.P(id="injury-title", className="paragraph-style"),
                            ]),

                            dcc.Tabs(
                                id='injury-tabs',
                                value='sunburst',
                                children=[
                                    dcc.Tab(label='Sunburst', value='sunburst'),
                                    dcc.Tab(label='Sankey', value='sankey')
                                ],
                                className='custom-tabs'
                            ),
                            dcc.Graph(id='injury-graph', config={'staticPlot': True}),
                            html.Div(id="injury-description")
                        ]),]
                )
            ]
        )
])

@app.callback(
    Output('dynamic-title', 'children'),
    Input('year-slider', 'value')
)
def update_dynamic_title(year_range):
    """
    Updates the title displayed above the first graph based on the selected year range.

    Args:
        year_range (List[int]): A list containing the start and end year selected via the RangeSlider.

    Returns:
        str: A formatted string indicating the selected year(s) for display in the title.
    """
    year_start, year_end = year_range
    if year_start == year_end:
        return f"Nombre d'accidents par saison ({year_start})"
    else:
        return f"Nombre d'accidents par saison ({year_start}–{year_end})"

@app.callback(
    [Output('button-Hiver', 'className'),
     Output('button-Printemps', 'className'),
     Output('button-Été', 'className'),
     Output('button-Automne', 'className'),
     Output('figure1', 'figure')],
    [Input('year-slider', 'value'),
     Input('button-Hiver', 'n_clicks'),
     Input('button-Printemps', 'n_clicks'),
     Input('button-Été', 'n_clicks'),
     Input('button-Automne', 'n_clicks')],
    [State('button-Hiver', 'className'),
     State('button-Printemps', 'className'),
     State('button-Été', 'className'),
     State('button-Automne', 'className'),
     State('figure1', 'figure')],
)
def update_figure_1(year_range, winterClick, springClick, summerClick, autumnClick,
                        winterClass, springClass, summerClass, autumnClass, figure):
    """
    Updates the seasonal selection buttons and the associated figure (figure1)
    based on the selected year range and the user's button interactions.

    This function toggles the class of each seasonal button when clicked,
    determines which seasons are selected, and redraws the figure using
    data filtered by the selected seasons and years.

    Args:
        year_range (List[int]): Start and end year from the range slider.
        winterClick (int): Winter button.
        springClick (int): Spring button.
        summerClick (int): Summer button.
        fallClick (int): Fall button.
        winterClass (str): Current CSS class for the Winter button.
        springClass (str): Current CSS class for the Spring button.
        summerClass (str): Current CSS class for the Summer button.
        fallClass (str): Current CSS class for the Fall button.
        figure (dict): Current Plotly figure (figure1) to be updated.

    Returns:
        Tuple[str, str, str, str, go.Figure]: Updated class names for each seasonal button
        and the updated Plotly figure reflecting the new seasonal and year filters.
    """
    triggered_id = ctx.triggered_id
    start_year, end_year = year_range

    def toggle_class(current_class):
        return "button-season selected" if "selected" not in current_class else "button-season not-select"

    class_dict = {
        'Hiver': toggle_class(winterClass) if triggered_id == 'button-Hiver' else winterClass,
        'Printemps': toggle_class(springClass) if triggered_id == 'button-Printemps' else springClass,
        'Été': toggle_class(summerClass) if triggered_id == 'button-Été' else summerClass,
        'Automne': toggle_class(autumnClass) if triggered_id == 'button-Automne' else autumnClass,
    }
    selected_seasons = [season for season, c in class_dict.items() if 'selected' in c]
    
    fig = go.Figure()

    if len(selected_seasons) == 0:
        fig.update_layout(
            title='Veuillez sélectionner au moins une saison.',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(
                text="Aucune donnée à afficher",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20)
            )]
        )
    
    else :
        fig = figure_1.draw(figure, data_fig_1, start_year, end_year, selected_seasons)

    return (
        class_dict['Hiver'],
        class_dict['Printemps'],
        class_dict['Été'],
        class_dict['Automne'],
        fig
    )

@app.callback(
    Output('radar-graph', 'figure'),
    [Input('day-checklist', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_figure_2(selected_days, start_date, end_date):
    """
    Updates the radar chart (figure 2) based on the selected days of the week
    and a specified date range.

    If any required input is missing (no day selected or invalid date range),
    an empty figure with a message is returned.

    Args:
        selected_days (Optional[List[str]]): List of selected days from the checklist.
        start_date (Optional[str]): Start date from the date range picker (ISO format).
        end_date (Optional[str]): End date from the date range picker (ISO format).

    Returns:
        go.Figure: A Plotly radar figure showing crash statistics for the selected days and dates,
                   or an empty figure with an instructional message if inputs are invalid.
    """
    if not selected_days or not start_date or not end_date:
        fig = go.Figure()
        fig.update_layout(
            title='Veuillez sélectionner au moins un jour et un intervalle de dates.',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(
                text="Aucune donnée à afficher",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=20)
            )]
        )
        return fig

    mask = (data_fig_2['crash_date'] >= pd.to_datetime(start_date)) & (data_fig_2['crash_date'] <= pd.to_datetime(end_date))
    filtered_df = data_fig_2.loc[mask]

    return figure_2.draw(filtered_df, selected_days)

@app.callback(
    Output("injury-graph", "figure"),
    Input("injury-tabs", "value")
)
def switch_injury_graph(selected_tab):
    """
    Switches the injury graph based on the selected tab.

    If the 'sankey' tab is selected, it returns the alternative Sankey diagram.
    Otherwise, it returns the sunburst diagram figure.

    Args:
        selected_tab (str): The value of the currently selected tab.

    Returns:
        go.Figure: The corresponding injury figure to display.
    """
    if selected_tab == 'sankey':
        return fig4_alt
    return fig4

@app.callback(
    [Output("injury-title", "children"),
     Output("injury-description", "children")],
    Input("injury-tabs", "value")
)
def update_injury_section(tab_value):
    """
    Updates the injury section's title and descriptive text based on the selected tab.

    Args:
        tab_value (str): The selected tab, either "sunburst" or "sankey".

    Returns:
        Tuple[str, List[html.P]]: A tuple containing the section title and a list of paragraphs as Dash HTML components.
    """
    if tab_value == "sunburst":
        title = "Le récit se termine avec ce qui compte : les vies humaines. Ce Sunburst montre le lien entre causes et gravité des blessures."
        paragraphs = [ html.P("Chaque accident n’est pas qu’un point dans un graphique, mais une vie bouleversée.", className="paragraph-style"),
            html.P("Le Sunburst ci-dessous plonge au cœur de cette réalité : il relie chaque catégorie de blessure — des blessures légères aux cas les plus graves — aux causes qui les ont provoquées.", className="paragraph-style"),
            html.P("Ce qui ressort clairement de cette visualisation, c’est que les blessures sont avant tout le reflet des erreurs humaines. La conduite imprudente, qui englobe des comportements comme l'excès de vitesse ou la négligence, occupe une place prépondérante, notamment parmi les blessures légères. Cela souligne l'importance de la vigilance et de la responsabilité des conducteurs au quotidien.", className="paragraph-style"),
            html.P("Les infractions au code de la route et les distractions, bien que souvent banalisées, figurent également parmi les causes fréquentes d’accidents. Cela révèle un rapport parfois trop détendu à la sécurité, où certains comportements, bien que risqués, sont perçus comme acceptables dans notre routine.", className="paragraph-style"),
            html.P("Cependant, lorsque la gravité des blessures augmente, le profil des causes se transforme. Les comportements à risque tels que la conduite sous influence ou l’alcool au volant pèsent bien plus lourd parmi les blessures graves ou mortelles. Ces erreurs humaines ont des conséquences bien plus tragiques, amplifiées par la négligence ou le manque de jugement.", className="paragraph-style"),
            html.P("Ce diagramme nous invite à reconsidérer nos comportements sur la route. Car derrière chaque « cause », il y a une histoire, un trajet interrompu, une famille marquée. Les données ne sont pas simplement des chiffres ; elles racontent des vies, des choix et des erreurs humaines qui auraient pu être évitées.", className="paragraph-style")
        ]
    else:
        title = "Une lecture alternative sous forme de Sankey : des blessures jusqu’aux causes, cette fois en flux."
        paragraphs = [
            html.P("Cette visualisation Sankey nous permet de voir les causes des blessures de manière claire et fluide : elle commence par l'impact humain, puis nous guide vers les facteurs qui l'ont provoqué.", className="paragraph-style"),
            html.P("À gauche, les blessures — légères, graves ou mortelles — sont représentées, et à droite, les causes se relient aux blessures, montrant comment elles contribuent aux drames.", className="paragraph-style"),
            html.P("Le flux le plus dense provient des blessures légères, ce qui montre que la majorité des accidents restent heureusement sans gravité, mais la réalité est plus complexe.", className="paragraph-style"),
            html.P("Le diagramme ne laisse pas place à l'illusion : lorsqu'on s'approche des blessures graves et mortelles, les causes deviennent bien plus spécifiques, liées à des comportements à risque comme la conduite imprudente, les excès de vitesse ou les infractions au code de la route.", className="paragraph-style"),
            html.P("Ce Sankey ne se limite pas à être un simple outil d'analyse : il raconte une histoire. Une histoire de moments perdus, de choix erronés, et de conséquences souvent irréversibles. Il rappelle que derrière chaque chiffre, il y a une vie bouleversée par une erreur humaine.", className="paragraph-style")
        ]
    return title, paragraphs

data = load_data()

data_fig_1, data_fig_2, data_fig_3, data_fig_4 = prep_data(data)

# Call the function to initialize the figures
fig1, fig2, fig3, fig4, fig4_alt = init_figure(data_fig_1, data_fig_2, data_fig_3, data_fig_4)

# Set up the app layout
app.layout = init_app_layout(fig1, fig2, fig3)
