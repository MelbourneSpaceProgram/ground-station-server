import dash
import pandas as pd
import requests
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px

BACKEND = "http://host.docker.internal:8888"

app = dash.Dash(__name__, update_title=None)

map_fig = go.Figure(go.Scattergeo())
map_fig.update_geos(projection_type="natural earth")
map_fig.update_layout(height=300, margin={"t": 0, "b": 0, "l": 0, "r": 0}, uirevision='yes')

map_fig.add_trace(
    go.Scattergeo(
        lat=[-37.814],
        lon=[144.963],
        mode="markers",
        hoverinfo="text",
        text=["Ground station"],
    )
)

map_fig.add_trace(
    go.Scattergeo(
        lat=[0],
        lon=[0],
        mode="lines+markers",
    )
)

app.layout = html.Div(
    children=[
        html.H1(children="ACRUX-2 Ground Station"),
        html.Button("Refresh", id="refresh", n_clicks=0),
        dcc.Graph(id="world-map", figure=map_fig),
        html.H2(children="Satellites"),
        html.Div(
            id="sat-form",
            style={"padding": "10px"},
            children=[
                dcc.Input(id="add-sat", type="text", placeholder="NORAD ID"),
                dcc.Input(id="add-name", type="text", placeholder="Name"),
                dcc.Dropdown(
                    id="add-pipeline", options=[{"label": "NOAA", "value": "NOAA"}]
                ),
                html.Button("Add", id="add", n_clicks=0),
                dcc.Dropdown(id="delete-sat"),
                html.Button("Delete", id="delete", n_clicks=0),
            ],
        ),
        dash_table.DataTable(id="table"),
        dcc.Interval(id='interval', interval=500, n_intervals=0),
    ]
)

latlon_cache = {}

@app.callback(Output('world-map', 'extendData'), Input('interval', 'n_intervals'))
def satellite_pos(n):
    if bool(latlon_cache):
        data = latlon_cache['43013']
        dict(x=[data[1][1], data[1][1000]], y=[data[2][1], data[2][2000]]), [1]

@app.callback(
    Output("table", "data"), Output("table", "columns"), Input("refresh", "n_clicks")
)
def update_satellites(n_clicks):
    sats = requests.get(BACKEND + "/satellites")
    df = pd.DataFrame(sats.json())

    data = df.to_dict(orient="records")
    columns = [{"name": col, "id": col} for col in df.columns]

    for sat in data:
        sat_id = sat['id']
        # save latlon
        latlon_cache[sat_id] = pd.DataFrame(requests.get(BACKEND + "/satellites/" + sat_id + "/latlon").json())

    return data, columns


@app.callback(Output("delete-sat", "options"), Input("table", "data"))
def update_dropdown(data):
    if data is None:
        return []
    return [{"label": sat["name"], "value": sat["id"]} for sat in data]


@app.callback(
    Output("refresh", "n_clicks"),
    Input("add", "n_clicks"),
    Input("delete", "n_clicks"),
    State("add-sat", "value"),
    State("add-name", "value"),
    State("add-pipeline", "value"),
    State("delete-sat", "value"),
)
def edit_satellites(add_btn, del_btn, add_val, name, pipeline, del_val):
    ctx = dash.callback_context

    if ctx.triggered:
        print(ctx.triggered)
        if ctx.triggered[0]["prop_id"].split(".")[0] == "add":
            add_satellite(add_val, name, pipeline)
        else:
            delete_satellite(del_val)

    return add_btn + del_btn


def add_satellite(sat_id, name, pipeline):
    if sat_id is not None:
        requests.post(
            BACKEND + "/satellites",
            data={"id": sat_id, "name": name, "pipeline": "NOAA"},
        )


def delete_satellite(sat_id):
    if sat_id is not None:
        requests.delete(BACKEND + "/satellites/" + sat_id)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
