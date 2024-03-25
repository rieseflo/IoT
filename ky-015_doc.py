#terminal:
"""
sudo apt-get update
sudo apt-get install build-essential python-dev
sudo apt install gpiod
sudo pip3 install adafruit-circuitpython-dht
"""
#programm start
"""
sudo python3 KY015-RPi.py
"""

import time
import board
import adafruit_dht

# Initialisieren Sie das dht-Gerät, wobei der Datenpin mit Pin 16 (GPIO 23) des Raspberry Pi verbunden ist:
dhtDevice = adafruit_dht.DHT11(board.D23)

# Sie können DHT22 use_pulseio=False übergeben, wenn Sie pulseio nicht verwenden möchten.
# Dies kann auf einem Linux-Einplatinencomputer wie dem Raspberry Pi notwendig sein,
# aber es wird nicht in CircuitPython funktionieren.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        # Drucken der Werte über die serielle Schnittstelle
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))

    except RuntimeError as error:
        # Fehler passieren ziemlich oft, DHT's sind schwer zu lesen, einfach weitermachen
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)