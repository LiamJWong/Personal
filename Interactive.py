import pandas as pd
import plotly.express as px

import numpy as np
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


#Import/format Data data --------------------------------------------
steamdata = pd.read_csv('ensf-310-f2021-project3-ljw\lifetime_concurrent_users_steam.csv', header=0)

#change time column format
steamdata['DateTime'] = pd.to_datetime(steamdata['DateTime'])

#two week rolling average
steamdata['rolling_users'] = steamdata['Users'].rolling(14).mean()

#locate years 2020-2022
steamdata['2020-2022']= steamdata['DateTime'].loc[5834:6475]
steamdata['2020-2022-Users'] = steamdata['Users'].loc[5834:6475]

#fill empty cells with 0
steamdata['2020-2022-Users'] = steamdata['2020-2022-Users'].fillna(0)

steamdata['Concurrent After Covid']= steamdata['In-Game'].loc[5053:]
steamdata['Concurrent After Covid'].loc[5053:5904] = None
steamdata['Concurrent Before Covid'] = steamdata['In-Game'].loc[5053:]
steamdata['Concurrent Before Covid'].loc[5900:] = None
steamdata['DateTime for in Game'] = steamdata['DateTime'].loc[5053:]

# App Layout----------------------------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Steam Users Over Time", style={'text-align': 'center'}),

    dcc.Dropdown(id="select_graph",
                 options=[
                     {"label": "Active Users Over Time", "value": 'Active Users Over Time'},
                     {"label": "Total Users Over Time", "value": 'Total Users Over Time'},
                     {"label": "Curve Fitting Users", "value": 'Scatterplot of Total Users from 2020-2021'}],
                multi=False,
                value='Active Users Over Time',
                style={'width': "60%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='steam_graph', figure={})

])


# Callback ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='steam_graph', component_property='figure')],
    [Input(component_id='select_graph', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)

    container = "Now Presenting: {}".format(option_slctd)

    if option_slctd == 'Active Users Over Time':
        #This is for active users
        fig = px.line(steamdata, x='DateTime for in Game', y=['Concurrent After Covid','Concurrent Before Covid'], title='Concurrent Users Over Time')
    
    elif option_slctd == 'Total Users Over Time':
        #This is for total users
        fig = px.line(steamdata, x='DateTime', y=['Users', 'rolling_users'], title='Total Users Over Time')
    
    else:
        #If not 1 and 2 then Curve Fit Line
        #statsmodel had to be installed to calculate trendline!
        fig = px.scatter(steamdata, x='2020-2022', y='2020-2022-Users', trendline='rolling', trendline_options=dict(window=10), 
            trendline_color_override='black', color_discrete_sequence=['red'], title='Total Users from 2020-2021'
        )

    return container, fig

if __name__ == '__main__':
    app.run_server(debug=True)
    