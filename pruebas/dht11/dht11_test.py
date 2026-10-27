import pigpio
import DHT11
import time

# Initialize pigpio and DHT11
pi = pigpio.pi()
SENSOR_PIN = 4  # GPIO 4 (BCM numbering)
sensor = DHT11.DHT11(pi, SENSOR_PIN)

# Read data
while True:
    result = sensor.read()
    if result.valid:
        print(f"Temperature: {result.temperature:.1f}°C")
        print(f"Humidity: {result.humidity:.1f}%")
    else:
        print("Failed to get reading. Trying again...")
    time.sleep(2)  # Wait 2 seconds before the next reading