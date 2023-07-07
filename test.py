import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample DataFrame
df = pd.DataFrame({
    'Date': pd.date_range(start='2023-06-05', end='2023-06-30', freq='D'),
    'Value': [1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0]
})

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Pie Chart with DatePicker"), width={"size": 6, "offset": 3}),
            justify="center",
            className="mb-4 mt-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Label("Start Date"),
                    width={"size": 2},
                    className="text-right"
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='start-date-picker',
                        min_date_allowed=pd.to_datetime('2023-06-05'),
                        max_date_allowed=pd.to_datetime('2023-07-31'),
                        initial_visible_month=pd.to_datetime('2023-06-05'),
                        date=pd.to_datetime('2023-06-05')
                    ),
                    width={"size": 2},
                ),
                dbc.Col(
                    html.Label("End Date"),
                    width={"size": 2},
                    className="text-right"
                ),
                dbc.Col(
                    dcc.DatePickerSingle(
                        id='end-date-picker',
                        min_date_allowed=pd.to_datetime('2023-06-05'),
                        max_date_allowed=pd.to_datetime('2023-07-31'),
                        initial_visible_month=pd.to_datetime('2023-06-05'),
                        date=pd.to_datetime('2023-06-30')
                    ),
                    width={"size": 2},
                ),
            ],
            justify="center",
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='pie-chart',
                    responsive=True
                ),
                width={"size": 6, "offset": 3},
            ),
            justify="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [dash.dependencies.Input('start-date-picker', 'date'),
     dash.dependencies.Input('end-date-picker', 'date')]
)
def update_pie_chart(start_date, end_date):
    filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
    value_counts = filtered_df['Value'].value_counts()
    count_of_1 = value_counts.get(1, 0)
    total_days = len(filtered_df)
    fig = px.pie(
        values=[count_of_1, total_days - count_of_1],
        names=['1', '0'],
        hole=0.7,
        color=['blue', 'gray'],
        labels={'label': 'Value'},
        title=f"<b>{count_of_1}/{total_days}</b>",
        #title_font=dict(size=20),
        opacity=0.7,
        template="plotly_white"
    )

    fig.update_traces(
        textposition='inside',
        textinfo='none'
    )

    fig.update_layout(
        autosize=True,
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=False,
        annotations=[
            dict(
                text="<b>Count of 1 / Total Days</b>",
                showarrow=False,
                font=dict(size=16),
                x=0.5,
                y=0.5
            )
        ],
        #rotation=90
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
