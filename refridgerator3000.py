from sense_hat import SenseHat

sense = SenseHat()

#Print Text
#sense.show_message("Hallo Elias!")

# Read temperature
temperature = sense.get_temperature()
print("Temperature: {:.2f} C".format(temperature))

#Read humidity
humidity = sense.get_humidity()
print("Humidity: {:.2f} %".format(humidity))

#Read pressure
pressure = sense.get_pressure()
print("Pressure: {:.2f} Millibars".format(pressure))

#Read accelerometer data
acceleration = sense.get_accelerometer()
print(acceleration)

#Read gyroscope data
gyroscope = sense.get_gyroscope()
print("Gyroscope: (pitch={:.2f}, roll={:.2f}, yaw={:.2f})".format(gyroscope['pitch'], gyroscope['roll'], gyroscope['yaw']))

#Read magnetometer data
magnetometer = sense.get_compass()
print("Magnetometer: {:.2f} Degrees".format(magnetometer))
