import paho.mqtt.client as mqtt
import random
import time

# Configuración del broker MQTT
BROKER = "192.168.111.107"
PORT = 1883
TOPIC_SUBSCRIBE = "Entrada/01"
TOPIC_PUBLISH = "Salida/01"
CLIENT_ID = "raspberryClient"

# Variable para almacenar el último mensaje recibido
var = 0
resultS = ""

# Callback cuando se recibe un mensaje
def on_message(client, userdata, message):
    global var, resultS
    payload_string = message.payload.decode("utf-8")
    
    try:
        var = int(payload_string)
    except ValueError:
        var = 0  # Si no es un número, se asigna 0
    
    resultS = payload_string
    print(f"Mensaje recibido en {message.topic}: {resultS}")

# Configuración del cliente MQTT
client = mqtt.Client(CLIENT_ID)
client.on_message = on_message

def connect_mqtt():
    """ Intenta conectarse al broker MQTT """
    while True:
        try:
            client.connect(BROKER, PORT)
            print("Conectado a MQTT")
            return
        except Exception as e:
            print(f"Fallo en la conexión: {e}, reintentando en 5 segundos...")
            time.sleep(5)

# Conectar al broker y suscribirse al topic
connect_mqtt()
client.subscribe(TOPIC_SUBSCRIBE)
client.loop_start()  # Inicia la gestión automática de mensajes

# Loop principal
try:
    while True:
        # Publica un valor aleatorio
        datos = f"Valor random: {random.randint(1, 100)}"
        client.publish(TOPIC_PUBLISH, datos)
        print(f"Publicado: {datos}")
        time.sleep(0.125)
except KeyboardInterrupt:
    print("Desconectando...")
    client.loop_stop()
    client.disconnect()
