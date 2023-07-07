# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 14:47:58 2023

@author: nabil
"""

# driver script
from utils.AndroidDat import AndroidDat
from utils.utils_class import read_dat
import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px

# global variables
#
fname = "https://raw.githubusercontent.com/nabila-shawki/healthdata-dash-plotly/main/data/week_3.csv"
start_date = pd.to_datetime('2023-06-05')
end_date = pd.to_datetime('2023-07-30')
target_count = 2000

# get the filtered dat
#
dat = read_dat(fname, start_date, end_date, target_count)
print(dat.filtered_df.shape)

# create a dash app
#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.PULSE],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

# the datepicker
#
start_date = dcc.DatePickerSingle(
            id='start-date-picker',
            min_date_allowed=pd.to_datetime('2023-06-05'),
            max_date_allowed=pd.to_datetime('2023-07-31'),
            initial_visible_month=pd.to_datetime('2023-06-05'),
            date=pd.to_datetime('2023-06-05'),
            persistence=True,
            persisted_props=['date'],
            persistence_type='session'
            )
                    
end_date = dcc.DatePickerSingle(
                        id='end-date-picker',
                        min_date_allowed=pd.to_datetime('2023-06-05'),
                        max_date_allowed=pd.to_datetime('2023-07-31'),
                        initial_visible_month=pd.to_datetime('2023-06-05'),
                        date=pd.to_datetime('2023-06-30'),
                        persistence=True,
                        persisted_props=['date'],
                        persistence_type='session'
                    )

# create a layout
#
app.layout = dbc.Container(
    [
        # title
        #
        dbc.Row(
            dbc.Col(html.H1("The Remote Monitoring Dashboard"), width={"size": 6, "offset": 3}),
            
            className="text-center text-primary mb-4",
        ),

        # the calendar
        #
        dbc.Row([
                dbc.Col(
                    html.H4("Start Date"),
                    width="auto",
                    
                    className="text_left"
                ),
                dbc.Col(
                    start_date,
                    width="auto",
                    className="text_left"
                ),
 
                dbc.Col(
                    html.H4("End Date"),
                    width="auto",
                    
                    className="text_left"
                ),
                dbc.Col(
                    end_date,
                    width="auto",
                ),
            ],
            justify="left",
            align="center"
            #className="g-0",
        ),

        dbc.Row([
            dbc.Col(
                dcc.Graph(                    
                    id='pie-chart',
                    responsive=True
                ),
                width={"size": 8},
            ),
        ],
            justify="left",
            className="mb-4",
        ),


    ],
    fluid=True,
)


@app.callback(
    # dash.dependencies.Output('pie-chart', 'figure'),
    # [dash.dependencies.Input('start-date-picker', 'date'),
    #  dash.dependencies.Input('end-date-picker', 'date')]
    Output('pie-chart', 'figure'),
    Input('start-date-picker', 'date'),
    Input('end-date-picker', 'date'),    
)
def update_pie_chart(start_date, end_date):
    df = dat.filtered_df
    filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
    value_counts = filtered_df['Target Met'].value_counts()
    value_counts = value_counts.sort_index(ascending=False)
    
    fig = px.pie(
        value_counts,
        values=value_counts.values,
        names=value_counts.index,
        hole=0.7,
        color=value_counts.index,
        color_discrete_map={  0: 'gray', 1: 'blue'},
        labels={'label': 'Value'},
        
    )
    # hiding legend in pyplot express.
    fig.update_traces(showlegend=False,
                      textinfo='none',
                      sort=False
                      )
    return fig

if __name__=='__main__':
    app.run_server(debug=True)
