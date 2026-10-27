import dash
from dash import dcc, html, Input, Output, State
import dash_extendable_graph as deg
import plotly.graph_objects as go
import paho.mqtt.client as mqtt
import threading
import time
import csv
az = {
    'margin': '10px',
    'font-size': '22px',
    'padding': '5px 10px',
    'background-color': '#6697ff',
    'color': 'white',
    'border': 'none',
    'border-radius': '10px',
    "cursor": "pointer",
}


MQTT_BROKER = "localhost"  
MQTT_PORT = 1883
MQTT_TOPIC = "#"
USERNAME="groundstation0"
PASSWORD ="1234"

DATA_NAMES = [
    "Temperatura interna", "Aceleración X", "Aceleración Y", "Aceleración Z",
    "Intensidad UV", "Altitud", "Latitud", "Longitud",
    "Vel. Angular X", "Vel. Angular Y", "Vel. Angular Z", "Voltaje de la batería", "Velocidad de descenso"
]


data_storage = {name: {"x": [], "y": []} for name in DATA_NAMES}


selected_data = "Temperatura interna"

def leer_csv_distribuir(nombre_archivo):
    datos = [[] for _ in range(13)]  # Crear 13 listas vacías
    
    with open(nombre_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            for i, valor in enumerate(fila):
                datos[i % 13].append(valor)  # Distribuir los datos en 13 listas
    
    return datos

# Ejemplo de uso
nombre_archivo = "datos.csv"
datos = leer_csv_distribuir(nombre_archivo)
for i, arreglo in enumerate(datos):
    print(f"Arreglo {i+1}:", arreglo)


    #except Exception as e:
     #   print(f"Error procesando mensaje MQTT: {e}")


#mqtt_client = mqtt.Client()
#mqtt_client.username_pw_set(USERNAME, PASSWORD) 
#mqtt_client.on_message = on_message
#mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
#mqtt_client.subscribe(MQTT_TOPIC)

#mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
#mqtt_thread.daemon = True
#mqtt_thread.start()

# Ejemplo de uso


app = dash.Dash(__name__)


app.layout = html.Div([
html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%'}, children=[
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'width': '60%'}, children=[
        html.Button(name, id=f"btn-{name}", n_clicks=0, style=az)
        for name in DATA_NAMES
        ]),
        html.Div(style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}, children=[
            html.Button('INICIAR TRANSMISIÓN', id='btn-iniciar', n_clicks=0, style={
                "margin": "10px", "font-size": "30px", "padding": "10px 25px", "background-color": "#b6ee83",
                "color": "black", "border": "none", "border-radius": "10px", "cursor": "pointer"
            }),
            html.Button('PAUSAR/REANUDAR TRANSMISIÓN', id='btn-pausar', n_clicks=0, style={
                "margin": "10px", "font-size": "30px", "padding": "10px 25px", "background-color": "#EEBD62",
                "color": "black", "border": "none", "border-radius": "10px", "cursor": "pointer"
            }),
            html.Button('TERMINAR TRANSMISIÓN', id='btn-terminar', n_clicks=0, style={
                "margin": "10px", "font-size": "30px", "padding": "10px 25px", "background-color": "#ff5c5c",
                "color": "black", "border": "none", "border-radius": "10px", "cursor": "pointer"
            }),
        ]),
    ]),
    dcc.Store(id="selected-data", data="Temperatura interna"), 
    deg.ExtendableGraph(id="live-graph", figure=go.Figure(), style={"height": "60vh"}),
    dcc.Interval(id="interval-component", interval=250, n_intervals=0) 
])


@app.callback(
    Output("selected-data", "data"),
    [Input(f"btn-{name}", "n_clicks") for name in DATA_NAMES],
    prevent_initial_call=True
)
def update_selected_data(*args):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        return button_id.replace("btn-", "")
    return dash.no_update


@app.callback(
    Output("live-graph", "figure"),
    [Input("interval-component", "n_intervals"), State("selected-data", "data")]
)
def update_graph(n, selected_data):
    x = data_storage[selected_data]["x"]
    y = data_storage[selected_data]["y"]

    fig = go.Figure(data=go.Scatter(x=x, y=y, mode="lines"))
    fig.update_layout(title=f"Gráfica de {selected_data} en tiempo real")

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)