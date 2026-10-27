import random
import dash
import plotly
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

X = list()
X.append(0)
Y = list()
Y.append(0)
app = dash.Dash(__name__, suppress_callback_exceptions=True,)
app.layout = html.Div([html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='graph-update',
        interval=0.05 * 1000
    ),
])
])

latest_sno = 0


@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):
    
    X.append(X[-1]+1)
    if len(X)>10:
        X.pop(0)
    Y.append(0+random.randint(-2,2))
    data = plotly.graph_objs.Scatter(
        x=X,
        y=Y,
        name='lines',
        mode='lines'
    )
    if (len(X)) > 1000:
        x_l = max(X) - 1000
    else:
        x_l = 0
    return {'data': [data], 'layout': go.Layout(title="BMS_01_CellVolt_AVG01",
                                                xaxis=dict(range=[x_l, max(X) + 1]),
                                                yaxis=dict(range=[min(Y) - 0.15, max(Y) + 1]),
                                                yaxis_title="Voltage in (V)",
                                                xaxis_title="TIME",
                                                )}
if __name__ == '__main__':
    app.run_server(debug=True,port = 5050)