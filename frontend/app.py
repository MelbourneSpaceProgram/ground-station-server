import dash
import pandas as pd
import requests
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='ACRUX-2 Ground Station'),

    html.Button('Refresh', id='refresh', n_clicks=0),

    html.H2(children='Satellites'),

    html.Div(
        id='sat-form',
        style={'padding': '10px'},
        children=[
            dcc.Input(id='add-sat', type='text', placeholder="NORAD ID"),
            dcc.Input(id='add-name', type='text', placeholder="Name"),
            dcc.Dropdown(id='add-pipeline', options=[{'label': 'NOAA', 'value': 'NOAA'}]),
            html.Button('Add', id='add', n_clicks=0),



            dcc.Dropdown(id='delete-sat'),
            html.Button('Delete', id='delete', n_clicks=0)
        ]),

    dash_table.DataTable(id='table')
])


@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('refresh', 'n_clicks')
)
def update_satellites(n_clicks):
    sats = requests.get(
        "http://host.docker.internal:5000/satellites"
    )
    df = pd.DataFrame(sats.json())

    data = df.to_dict(orient='records')
    columns = [{'name': col, 'id': col} for col in df.columns]

    return data, columns


@app.callback(
    Output('delete-sat', 'options'),
    Input('table', 'data')
)
def update_dropdown(data):
    if data is None:
        return []
    return [{'label': sat['name'], 'value': sat['id']} for sat in data]


@app.callback(
    Output('refresh', 'n_clicks'),
    Input('add', 'n_clicks'),
    Input('delete', 'n_clicks'),
    State('add-sat', 'value'),
    State('add-name', 'value'),
    State('add-pipeline', 'value'),
    State('delete-sat', 'value')
)
def edit_satellites(add_btn, del_btn, add_val, name, pipeline, del_val):
    ctx = dash.callback_context

    if ctx.triggered:
        if ctx.triggered[0]['prop_id'].split('.')[0] == "add":
            add_satellite(add_val, name, pipeline)
        else:
            delete_satellite(add_val)

    return add_btn + del_btn


def add_satellite(sat_id, name, pipeline):
    if sat_id is not None:
        requests.post("http://host.docker.internal:5000/satellites",
                      data={
                          'id': sat_id,
                          'name': name,
                          'pipeline': pipeline
                      })


def delete_satellite(sat_id):
    if sat_id is not None:
        requests.delete("http://host.docker.internal:5000/satellites/" + sat_id)


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050, debug=True)
    update_satellites()
