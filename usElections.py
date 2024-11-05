import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State

# Construct file path based on script location
current_directory = os.path.dirname(__file__)
csv_path = os.path.join(current_directory, 'usPresidentialResults.csv')
excel_path = os.path.join(current_directory, 'electoralData.xlsx')
electoral_df = pd.read_excel(excel_path)

# Load and preprocess the dataset
df = pd.read_csv(csv_path)
df['year'] = df['year'].astype(int)
df['pct'] = df['pct'].astype(float)
df['state'] = df['state'].str.title()

# Color cycle for interactive state changes
color_mapping = {
    'DEM-Solid': '#08306b',   # Dark Blue
    'DEM-Likely': '#2171b5',  # Medium Blue
    'DEM-Lean': '#6baed6',    # Light Blue
    'Tossup': '#808080',       # Grey
    'REP-Lean': '#fb6a4a',    # Light Red
    'REP-Likely': '#d7301f',  # Medium Red
    'REP-Solid': '#67000d',   # Dark Red
}

color_cycle = ['#08306b', '#2171b5', '#6baed6', '#808080', '#fb6a4a', '#d7301f', '#67000d']

# Map electoral votes and initial colors to each state
electoral_df['current_color'] = electoral_df['polls'].map(color_mapping)
electoral_df['electoral_votes'] = electoral_df['college']

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app with tabs for "Results" and "Evolution"
app.layout = html.Div([
    # Header with logos and title
    html.Div([
        html.Img(src="assets/presi.png", style={'height': '100px', 'float': 'left'}),
        html.Img(src="assets/usflag.png", style={'height': '100px', 'float': 'right'}),
        html.H1(
            "US Elections Dashboard",
            style={
                'textAlign': 'center', 
                'color': 'black', 
                'backgroundColor': 'gold',
                'padding': '0 20px', 
                'borderRadius': '10px', 
                'width': '50%', 
                'margin': '0 auto', 
                'height': '100px', 
                'lineHeight': '100px'  # Vertically centers the text
            }
        )
    ], style={'marginBottom': '20px'}),

    dcc.Tabs([
        #Results tabs
        dcc.Tab(label="Results", children=[
            html.Br(),
            #selector
            html.Div([
                html.Div([
                    html.Br(),
                    html.Button("Change Color", id="toggle-button", n_clicks=0),
                    html.Br(),html.Br(),
                    html.Label("Select Election Year"),
                    dcc.Slider(
                        id='year-slider-results',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=df['year'].max(),
                        marks={str(year): str(year) for year in df['year'].unique()},
                        step=None
                    ),
                    
                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top', 
                          'border': '2px solid black', 'padding': '20px', 'borderRadius': '5px'}),


                html.Div([
                    # Democratic section
                    html.Div([
                        html.Img(src="assets/dem.png", style={'height': '80px', 'margin-right': '15px'}),
                        html.Span(id='dem-states-count', style={'fontSize': '50px', 'color': 'black', 'margin-left': '30px'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'width': '45%', 'textAlign': 'center'}),

                    # VS image section, centered
                    html.Div([
                        html.Img(src="assets/versus.jpg", style={'height': '80px', 'margin': '0 auto'})  # Centered 'VS' image
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'width': '10%', 'textAlign': 'center'}),

                    # Republican section
                    html.Div([
                        html.Span(id='rep-states-count', style={'fontSize': '50px', 'color': 'black', 'margin-right': '30px'}),
                        html.Img(src="assets/rep.png", style={'height': '80px', 'margin-left': '15px'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'width': '45%', 'textAlign': 'center'})

                ], style={
                    'width': '40%',  # Adjusted width to fit and center within the page
                    'margin': '0 auto',  # Centers the entire block horizontally
                    'display': 'flex', 'justifyContent': 'space-between', 
                    'border': '6px dotted black', 'padding': '20px', 'borderRadius': '5px', 'textAlign': 'center'
                }),



                html.Div([
                    html.Div([
                        html.H2("WINNER", style={'fontSize': '24px', 'color': 'black', 'marginBottom': '10px'}),
                        html.Img(id='winner-logo', style={'height': '80px', 'marginBottom': '10px'}),
                        html.Span(id='winner-text', style={'fontSize': '20px', 'fontWeight': 'bold', 'color': 'black'})
                    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'textAlign': 'center', 'justifyContent': 'center'})
                ], style={
                    'width': '20%', 'margin': '0 auto', 
                    'border': '4px solid gold', 'padding': '20px', 'borderRadius': '5px', 'textAlign': 'center',
                }),
                
            ], style={'textAlign': 'center', 'width': '100%', 'display': 'flex', 'justify-content': 'space-between'}),

            html.Br(),

            #Map & tables
            html.Div([
                html.Div([
                    html.H4("Closest Races"),
                    html.Div(id='closest-races', style={'margin-top': '20px'}),
                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
                
                

                # Map in the center
                html.Div([
                    dcc.Graph(id='us-map-results', style={'height': '60vh'}),
                ], style={'width': '55%', 'display': 'inline-block', 'text-align': 'center'}),

                # Furthest Races table on the right
                html.Div([
                    html.H4("Furthest Races"),
                    html.Div(id='furthest-races', style={'margin-top': '20px'}),
                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'})
            ], style={'textAlign': 'center', 'width': '100%', 'display': 'flex', 'justify-content': 'space-around'}),

            # Additional graph below the main layout if needed
            html.Div([
                dcc.Graph(id='state-graph', style={'height': '60vh'})
            ], style={'width': '100%', 'display': 'inline-block', 'margin-top': '20px'}),
        ]),

        #Evolution tabs
        dcc.Tab(label="Evolution", children=[
            html.Br(),
            html.Div([
                html.Div([
                    html.Button("Change Color", id="toggle-button-2", n_clicks=0),
                    html.Br(),html.Br(),
                    html.Label("Select Data to Display"),
                    dcc.Dropdown(
                        id='data-selector',
                        options=[
                            {'label': 'REP', 'value': 'REP'},
                            {'label': 'DEM', 'value': 'DEM'},
                            {'label': 'Margin', 'value': 'MARGIN'}
                        ],
                        value='MARGIN'
                    ),
                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),

                html.Div([
                    html.Label("Select Start Year"),
                    dcc.Slider(
                        id='start-year-slider',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=df['year'].min(),
                        marks={str(year): str(year) for year in df['year'].unique()},
                        step=None
                    ),
                    html.Label("Select End Year"),
                    dcc.Slider(
                        id='end-year-slider',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=df['year'].max(),
                        marks={str(year): str(year) for year in df['year'].unique()},
                        step=None
                    ),
                    html.Br(),
                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'center'}),
                

                html.Br(),

                # Map & tables for evolution
                html.Div([
                    html.Div([
                        html.H4("DEM Sweeps"),
                        html.Div(id='closest-margin', style={'margin-top': '20px'}),
                    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
                    

                    # Map in the center
                    html.Div([
                        dcc.Graph(id='us-map-evolution', style={'height': '80vh'})
                    ], style={'width': '55%', 'display': 'inline-block', 'text-align': 'center'}),

                    # Furthest Races table on the right
                    html.Div([
                        html.H4("REP Sweeps"),
                        html.Div(id='furthest-margin', style={'margin-top': '20px'}),
                    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'})
                ], style={'textAlign': 'center', 'width': '100%', 'display': 'flex', 'justify-content': 'space-around'}),
            
            ]),
        ]),
    
        # Election Night tab
        dcc.Tab(label="Election Night", children=[
                        html.Br(),
            #selector
            html.Div([

                #Change color
                html.Div([
                    html.Br(),
                    html.Button("Change Color", id="toggle-button-3", n_clicks=0),
                    html.Br(),html.Br(),
                    html.Label("Select Election Year"),
                    dcc.Slider(
                        id='year-slider-results-3',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=df['year'].max(),
                        marks={str(year): str(year) for year in df['year'].unique()},
                        step=None
                    ),
                    
                ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top', 
                          'border': '2px solid black', 'padding': '20px', 'borderRadius': '5px'}),

                #Scoreboard
                html.Div([
                    # Democratic section
                    html.Div([
                        html.Img(src="assets/dem.png", style={'height': '80px', 'margin-right': '15px'}),
                        html.Span(id='dem-electoral-votes', style={'fontSize': '50px', 'color': 'black', 'margin-left': '30px'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'width': '45%', 'textAlign': 'center'}),

                    # VS image section, centered
                    html.Div([
                        html.Img(src="assets/versus.jpg", style={'height': '80px', 'margin': '0 auto'})  # Centered 'VS' image
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'width': '10%', 'textAlign': 'center'}),

                    # Republican section
                    html.Div([
                        html.Span(id='rep-electoral-votes', style={'fontSize': '50px', 'color': 'black', 'margin-right': '30px'}),
                        html.Img(src="assets/rep.png", style={'height': '80px', 'margin-left': '15px'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'width': '45%', 'textAlign': 'center'})

                ], style={
                    'width': '40%',  # Adjusted width to fit and center within the page
                    'margin': '0 auto',  # Centers the entire block horizontally
                    'display': 'flex', 'justifyContent': 'space-between', 
                    'border': '6px dotted black', 'padding': '20px', 'borderRadius': '5px', 'textAlign': 'center'
                }),

                #Winner
                html.Div([
                    html.Div([
                        html.H2("WINNER", style={'fontSize': '24px', 'color': 'black', 'marginBottom': '10px'}),
                        html.Img(id='winner-logo-2', style={'height': '80px', 'marginBottom': '10px'}),
                        html.Span(id='winner-text-2', style={'fontSize': '20px', 'fontWeight': 'bold', 'color': 'black'})
                    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'textAlign': 'center', 'justifyContent': 'center'})
                ], style={
                    'width': '20%', 'margin': '0 auto', 
                    'border': '4px solid gold', 'padding': '20px', 'borderRadius': '5px', 'textAlign': 'center',
                }),
                
            ], style={'textAlign': 'center', 'width': '100%', 'display': 'flex', 'justify-content': 'space-between'}),

            html.Br(),
            html.Br(),
            # Scoreboard for electoral votes
            # html.Div([
            #     html.H3("Election Night Dashboard", style={'textAlign': 'center'}),
            #     html.Div([
            #         html.Span("Democrats: ", style={'color': 'blue', 'fontSize': '24px'}),
            #         html.Div(id='dem-electoral-votes-2', style={'color': 'blue', 'fontSize': '24px'}),
            #         html.Span("vs", style={'fontSize': '24px', 'padding': '0 10px'}),
            #         html.Div(id='rep-electoral-votes-2', style={'color': 'red', 'fontSize': '24px'})
            #     ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'padding': '10px'}),
            # ]),

            # Interactive map for Election Night
            dcc.Graph(id='us-map-election-night'),

            # Hidden div for storing state colors and electoral counts
            dcc.Store(id='color-store', data=electoral_df.set_index('state_po')['current_color'].to_dict()),
            dcc.Store(id='vote-store', data=electoral_df.set_index('state_po')['electoral_votes'].to_dict())
        ]),

                #Results tabs

    ])
])

# Callback Results
@app.callback(
    [Output('winner-logo', 'src'), Output('winner-text', 'children')],
    [Input('dem-states-count', 'children'), Input('rep-states-count', 'children')]
)

def update_winner_logo_and_text(dem_count, rep_count):
    if int(dem_count) > int(rep_count):
        return "assets/dem.png", "Democratic Party"  # Path to Democratic logo and text
    else:
        return "assets/rep.png", "Republican Party"  # Path to Republican logo and text

@app.callback(
    [Output('us-map-results', 'figure'), Output('closest-races', 'children'),
    Output('furthest-races', 'children'), Output('state-graph', 'figure'),
    Output('dem-states-count', 'children'), Output('rep-states-count', 'children')],
    [Input('year-slider-results', 'value'), Input('toggle-button', 'n_clicks')]
)

def update_results_map(selected_year, n_clicks):
    # Filter data for the selected year
    filtered_df = df[df['year'] == selected_year]
    leading_party = filtered_df.loc[filtered_df.groupby('state_po')['pct'].idxmax()]

    # Calculate margin for each state by finding the difference between the top two candidates
    leading_party['second_pct'] = leading_party.apply(
        lambda row: filtered_df[(filtered_df['state_po'] == row['state_po']) & (filtered_df['party'] != row['party'])]['pct'].values[0],
        axis=1
    )
    leading_party['margin'] = ((leading_party['pct'] - leading_party['second_pct']).abs() * 100).round(2)

    # Determine closest races with limited columns and formatted margin
    closest_races = leading_party[['state', 'party', 'margin']].nsmallest(10, 'margin').reset_index(drop=True)
    closest_races['n'] = closest_races.index + 1  # Start numbering from 1

    furthest_races = leading_party[['state', 'party', 'margin']].nlargest(10, 'margin').reset_index(drop=True)
    furthest_races['n'] = furthest_races.index + 1  # Start numbering from 1

    # Generate the table for closest races
    closest_table = dash_table.DataTable(
        data=closest_races.to_dict('records'),
        columns=[
            {"name": "#", "id": "n"},
            {"name": "State", "id": "state"},
            {"name": "Winner", "id": "party"},
            {"name": "Margin (%)", "id": "margin"}
        ],
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'filter_query': '{party} = "DEM"'}, 'backgroundColor': 'lightblue'},
            {'if': {'filter_query': '{party} = "REP"'}, 'backgroundColor': 'lightcoral'}
        ]
    )

    # Generate the table for furthest races
    furthest_table = dash_table.DataTable(
        data=furthest_races.to_dict('records'),
        columns=[
            {"name": "#", "id": "n"},
            {"name": "State", "id": "state"},
            {"name": "Winner", "id": "party"},
            {"name": "Margin (%)", "id": "margin"}
        ],
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'filter_query': '{party} = "DEM"'}, 'backgroundColor': 'lightblue'},
            {'if': {'filter_query': '{party} = "REP"'}, 'backgroundColor': 'lightcoral'}
        ]
    )

    # Define 6-color scheme based on margin levels
    if n_clicks % 2 == 1: 
        conditions = [
            (leading_party['party'] == 'DEM') & (leading_party['margin'] <= 5),
            (leading_party['party'] == 'DEM') & (leading_party['margin'] > 5) & (leading_party['margin'] <= 15),
            (leading_party['party'] == 'DEM') & (leading_party['margin'] > 15),
            (leading_party['party'] == 'REP') & (leading_party['margin'] <= 5),
            (leading_party['party'] == 'REP') & (leading_party['margin'] > 5) & (leading_party['margin'] <= 15),
            (leading_party['party'] == 'REP') & (leading_party['margin'] > 15)
        ]
        colors = ['#a6cee3', '#1f78b4', '#08306b', '#fb9a99', '#e31a1c', '#67000d']
        color_labels = ['DEM Lean', 'DEM Likely', 'DEM Solid', 'REP Lean', 'REP Likely', 'REP Solid']
        leading_party['color'] = pd.Series([''] * len(leading_party))
        leading_party['color_label'] = pd.Series([''] * len(leading_party))
        
        for condition, color, label in zip(conditions, colors, color_labels):
            leading_party.loc[condition, 'color'] = color
            leading_party.loc[condition, 'color_label'] = label
    else:
        # Default bicolor scheme
        colors = {'DEM': 'blue', 'REP': 'red'}
        leading_party['color_label'] = leading_party['party']

    # Create custom hover text
    leading_party['hover_text'] = leading_party.apply(
        lambda row: (
            f"<b>{row['state']}</b><br><br>"
            f"REP: {100*row['pct']:.1f}%<br>"
            f"DEM: {100*row['second_pct']:.1f}%<br><br>"
            f"<b>+{row['margin']:.1f}% {row['party']}</b>"
        ),
        axis=1
    )

    #FIGURE

    fig = px.choropleth(
        leading_party,
        locations='state_po',
        locationmode="USA-states",
        color='color_label',
        color_discrete_map={
            'DEM Lean': '#a6cee3', 'DEM Likely': '#1f78b4', 'DEM Solid': '#08306b',
            'REP Lean': '#fb9a99', 'REP Likely': '#e31a1c', 'REP Solid': '#67000d',
            'DEM': 'blue', 'REP': 'red'
        },
        scope="usa",
        title=f"U.S. Presidential Election Results - {selected_year}",
        hover_name='state_po',
        custom_data=['hover_text']
    )
    fig.update_traces(hovertemplate='%{customdata[0]}')

    # Update layout to center title, add golden border, and raise legend position
    fig.update_layout(
        title={
            'text': f"{selected_year} Presidential Results",
            'x': 0.5, 'y': 0.9,
            'xanchor': 'center', 'yanchor': 'top',
            'font': {'size': 24, 'family': 'Arial, sans-serif', 'color': 'black'}
        },
        legend=dict(
            title_text='',
            itemsizing='constant',
            font=dict(size=16),
            orientation="h",
            yanchor="bottom",
            y=-0.1,  # Raise the legend slightly higher
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=0, r=0, t=50, b=20),  # Minimal margins around the map
        paper_bgcolor='white',               # Background of the entire map area
        plot_bgcolor='white',                # Background inside the map
        geo=dict(
            showframe=True,                  # Enable frame around the map
            framecolor="gold",               # Golden frame color
            framewidth=3,                    # Thicker frame width for visibility
            bgcolor='white'                  # Ensure map background remains white
        )
    )


    #PIE CHART
    state_wins = leading_party['party'].value_counts()  # Count states won by each party in the leading_party DataFrame

    # Prepare data for pie chart
    pie_data = pd.DataFrame({
        'party': ['DEM', 'REP'],
        'state_count': [
            state_wins.get('DEM', 0),  # Use 0 if no states won by DEM
            state_wins.get('REP', 0)   # Use 0 if no states won by REP
        ]
    })

    # Create the pie chart
    pie_fig = px.pie(
        pie_data,
        values='state_count',
        names='party',
        color='party',
        color_discrete_map={'DEM': 'blue', 'REP': 'red'},
        title="States Won by Party",
        hole=0.4  # For a donut chart
    )
    pie_fig.update_traces(textinfo='label+value', textfont_size=16)

    dem_count = (leading_party['party'] == 'DEM').sum()
    rep_count = (leading_party['party'] == 'REP').sum()
     
    return fig, closest_table, furthest_table, pie_fig, dem_count, rep_count

# Callback Evolution

@app.callback(
    [Output('us-map-evolution', 'figure'),
    Output('closest-margin', 'children'), Output('furthest-margin', 'children')],
    [Input('start-year-slider', 'value'), Input('end-year-slider', 'value'),
     Input('data-selector', 'value'), Input('toggle-button-2', 'n_clicks')]
)

def update_evolution_map(start_year, end_year, data_selector, n_clicks):
    # Filter data for the start and end years
    start_df = df[df['year'] == start_year]
    end_df = df[df['year'] == end_year]

    # Initialize variables
    fig = None
    closest_table = None
    sweeps_table = None

    # 1. Calculate margin if "MARGIN" is selected.
    if data_selector == 'MARGIN':
        # Calculate margin for each party in each year
        start_margin = start_df.groupby('state_po').apply(
            lambda x: x.loc[x['party'] == 'REP', 'pct'].values[0] - x.loc[x['party'] == 'DEM', 'pct'].values[0]
            if 'REP' in x['party'].values and 'DEM' in x['party'].values else 0
        ).reset_index(name='margin_start')
        
        end_margin = end_df.groupby('state_po').apply(
            lambda x: x.loc[x['party'] == 'REP', 'pct'].values[0] - x.loc[x['party'] == 'DEM', 'pct'].values[0]
            if 'REP' in x['party'].values and 'DEM' in x['party'].values else 0
        ).reset_index(name='margin_end')

        # Merge and calculate the change in margin
        margin_df = start_margin.merge(end_margin, on='state_po')
        margin_df['change'] = margin_df['margin_end'] - margin_df['margin_start']
        
        # Create custom hover text
        margin_df['hover_text'] = margin_df.apply(
            lambda row: (
                f"<b>{row['state_po']}</b><br><br>"
                f"{start_year}: {100*row['margin_start']:.1f}%<br>"
                f"{end_year}: {100*row['margin_end']:.1f}%<br><br>"
                f"Change: <b>{100*row['change']:+.1f}%</b>"
            ),
            axis=1
        )

        # 2. Define the color scheme for margin evolution
        if n_clicks % 2 == 1:
            # Use the 4-color scheme if the button is clicked
            conditions = [
                (margin_df['margin_start'] > 0) & (margin_df['margin_end'] > 0),  # REP to REP
                (margin_df['margin_start'] > 0) & (margin_df['margin_end'] <= 0), # REP to DEM
                (margin_df['margin_start'] <= 0) & (margin_df['margin_end'] > 0), # DEM to REP
                (margin_df['margin_start'] <= 0) & (margin_df['margin_end'] <= 0) # DEM to DEM
            ]
            colors = ['lightred', 'blue', 'red', 'lightblue']  # Light red, Dark red, Dark blue, Dark blue
            labels = ['REP to REP', 'REP to DEM', 'DEM to REP', 'DEM to DEM']
            margin_df['color_label'] = pd.Series([''] * len(margin_df))
            for condition, label in zip(conditions, labels):
                margin_df.loc[condition, 'color_label'] = label
        else:
            # Default bicolor scheme based on margin change
            margin_df['color_label'] = margin_df['change'].apply(lambda x: 'Positive' if x > 0 else 'Negative')

        # Define fig for margin evolution
        fig = px.choropleth(
            margin_df,
            locations='state_po',
            locationmode="USA-states",
            color='color_label',
            color_discrete_map={
                'REP to REP': '#ff9999',   # Light Red
                'REP to DEM': '#00008b',   # Dark Blue
                'DEM to REP': '#8b0000',   # Dark Red
                'DEM to DEM': '#add8e6',   # Light Blue
                'Positive': 'red',
                'Negative': 'blue'
            },
            scope="usa",
            title=f"Margin Change from {start_year} to {end_year}",
            hover_name='state_po',
            custom_data=['hover_text']
        )
        
        fig.update_traces(hovertemplate='%{customdata[0]}')

        # 3. Generate tables for closest and furthest margin changes
        closest_evolutions = margin_df.nsmallest(10, 'change').reset_index(drop=True)
        closest_evolutions['change'] = (closest_evolutions['change'] * 100).round(2)
        closest_evolutions['n'] = closest_evolutions.index + 1
        closest_evolutions['party'] = closest_evolutions['change'].apply(lambda x: 'REP' if x > 0 else 'DEM')

        closest_table = dash_table.DataTable(
            data=closest_evolutions.to_dict('records'),
            columns=[
                {"name": "#", "id": "n"},
                {"name": "State", "id": "state_po"},
                {"name": "Winner", "id": "party"},
                {"name": "Margin Change (%)", "id": "change"}
            ],
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'filter_query': '{party} = "DEM"'}, 'backgroundColor': 'lightblue'},
                {'if': {'filter_query': '{party} = "REP"'}, 'backgroundColor': 'lightcoral'}
            ]
        )

        # Generate the table for biggest sweeps
        biggest_sweeps = margin_df.nlargest(10, 'change').reset_index(drop=True)
        biggest_sweeps['change'] = (biggest_sweeps['change'] * 100).round(2)
        biggest_sweeps['n'] = biggest_sweeps.index + 1
        biggest_sweeps['party'] = biggest_sweeps['change'].apply(lambda x: 'REP' if x > 0 else 'DEM')

        sweeps_table = dash_table.DataTable(
            data=biggest_sweeps.to_dict('records'),
            columns=[
                {"name": "#", "id": "n"},
                {"name": "State", "id": "state_po"},
                {"name": "Winner", "id": "party"},
                {"name": "Margin Change (%)", "id": "change"}
            ],
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'filter_query': '{party} = "DEM"'}, 'backgroundColor': 'lightblue'},
                {'if': {'filter_query': '{party} = "REP"'}, 'backgroundColor': 'lightcoral'}
            ]
        )
    
    
    else:
        # 4. Process data for the selected party directly if "REP" or "DEM" is chosen in `data_selector`
        start_party_df = start_df[start_df['party'] == data_selector][['state_po', 'pct']].rename(columns={'pct': 'pct_start'})
        end_party_df = end_df[end_df['party'] == data_selector][['state_po', 'pct']].rename(columns={'pct': 'pct_end'})

        # Merge and calculate the change in percentage
        party_df = start_party_df.merge(end_party_df, on='state_po')
        party_df['change'] = party_df['pct_end'] - party_df['pct_start']

        # Create custom hover text
        party_df['hover_text'] = party_df.apply(
            lambda row: (
                f"<b>{row['state_po']}</b><br><br>"
                f"{start_year}: {100*row['pct_start']:.1f}%<br>"
                f"{end_year}: {100*row['pct_end']:.1f}%<br><br>"
                f"Change: <b>{100*row['change']:+.1f}%</b>"
            ),
            axis=1
        )

        # Define color scale based on the selected party with white centered at 0
        color_scale = [(0, 'blue'), (0.5, 'white'), (1, 'red')] if data_selector == 'REP' else [(0, 'red'), (0.5, 'white'), (1, 'blue')]

        fig = px.choropleth(
            party_df,
            locations='state_po',
            locationmode="USA-states",
            color='change',
            color_continuous_scale=color_scale,
            range_color=[-max(abs(party_df['change'])), max(abs(party_df['change']))],
            scope="usa",
            title=f"{data_selector} Change from {start_year} to {end_year}",
            hover_name='state_po',
            custom_data=['hover_text']
        )
        fig.update_traces(hovertemplate='%{customdata[0]}')

        # Update layout to center the title and format the map display
        fig.update_layout(
            title={
                'text': f"{data_selector} Change from {start_year} to {end_year}",
                'x': 0.5, 'y': 0.9,
                'xanchor': 'center', 'yanchor': 'top',
                'font': {'size': 24, 'family': 'Arial, sans-serif', 'color': 'black'}
            },
            legend=dict(
                title_text='Change',
                itemsizing='constant',
                font=dict(size=16),
                orientation="h",
                yanchor="bottom",
                y=-0.1,  # Raise the legend slightly higher
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=0, r=0, t=50, b=20),  # Minimal margins around the map
            paper_bgcolor='white',               # Background of the entire map area
            plot_bgcolor='white',                # Background inside the map
            geo=dict(
                showframe=True,                  # Enable frame around the map
                framecolor="gold",               # Golden frame color
                framewidth=3,                    # Thicker frame width for visibility
                bgcolor='white'                  # Ensure map background remains white
            )
        )

        # Generate tables for closest and furthest changes in selected party percentage
        closest_changes = party_df.nsmallest(10, 'change').reset_index(drop=True)
        closest_changes['change'] = (closest_changes['change'] * 100).round(2)
        closest_changes['n'] = closest_changes.index + 1  # Start numbering from 1
        closest_changes['party'] = data_selector

        closest_table = dash_table.DataTable(
            data=closest_changes.to_dict('records'),
            columns=[
                {"name": "#", "id": "n"},
                {"name": "State", "id": "state_po"},
                {"name": "Party", "id": "party"},
                {"name": "Change (%)", "id": "change"}
            ],
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'filter_query': '{party} = "DEM"'}, 'backgroundColor': 'lightblue'},
                {'if': {'filter_query': '{party} = "REP"'}, 'backgroundColor': 'lightcoral'}
            ]
        )

        furthest_changes = party_df.nlargest(10, 'change').reset_index(drop=True)
        furthest_changes['change'] = (furthest_changes['change'] * 100).round(2)
        furthest_changes['n'] = furthest_changes.index + 1
        furthest_changes['party'] = data_selector

        sweeps_table = dash_table.DataTable(
            data=furthest_changes.to_dict('records'),
            columns=[
                {"name": "#", "id": "n"},
                {"name": "State", "id": "state_po"},
                {"name": "Party", "id": "party"},
                {"name": "Change (%)", "id": "change"}
            ],
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'filter_query': '{party} = "DEM"'}, 'backgroundColor': 'lightblue'},
                {'if': {'filter_query': '{party} = "REP"'}, 'backgroundColor': 'lightcoral'}
            ]
        )

    return fig, closest_table, sweeps_table

 # Callback to handle color change on state click and update scoreboard

# Callback Election

@app.callback(
    [Output('winner-logo-2', 'src'), Output('winner-text-2', 'children')],
    [Input('dem-states-count', 'children'), Input('rep-states-count', 'children')]
)

def update_winner_logo_and_text(dem_votes, rep_votes):
    if int(dem_votes) > 269:
        return "assets/dem.png", "Democratic Party"  # Path to Democratic logo and text
    elif int(rep_votes) > 269:
        return "assets/rep.png", "Republican Party"  # Path to Republican logo and text
    else:
        return "assets/2024elections.jpg", "Too Early to Call"

@app.callback(
    [Output('us-map-election-night', 'figure'),
     Output('dem-electoral-votes', 'children'),
     Output('rep-electoral-votes', 'children'),
     Output('color-store', 'data')],
    [Input('us-map-election-night', 'clickData')],
    [State('color-store', 'data'), State('vote-store', 'data')]
)

def update_map_and_scoreboard(clickData, color_store, vote_store):
    if clickData:
        state_clicked = clickData['points'][0]['location']
        
        # Cycle to the next color for the clicked state
        current_color = color_store[state_clicked]
        #next_color = color_cycle[(color_cycle.index(current_color) + 1) % len(color_cycle)]
        
        print ("Index: ", color_cycle.index(current_color))
        print(state_clicked)

        if color_cycle.index(current_color) in [0,1,2]:
            next_color = color_cycle[3]
        elif color_cycle.index(current_color) == 3:
            next_color = color_cycle[4]
        else:
            next_color = color_cycle[2]
        
        color_store[state_clicked] = next_color

    # Recalculate electoral vote totals based on colors
    dem_votes = sum(vote_store[state] for state, color in color_store.items() if color in ['#08306b', '#2171b5', '#6baed6'])
    rep_votes = sum(vote_store[state] for state, color in color_store.items() if color in ['#fb6a4a', '#d7301f', '#67000d'])

    # Prepare map with updated colors
    map_fig = px.choropleth(
        electoral_df,
        locations='state_po',
        locationmode="USA-states",
        color=[color_store[state] for state in electoral_df['state_po']],
        color_discrete_map={c: c for c in color_cycle},  # Use cycle colors directly
        scope="usa",
        title="Election Night Map"
    )

    return map_fig, dem_votes, rep_votes, color_store                                                                        

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
