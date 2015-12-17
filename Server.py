from PinCreator import PinCreator
from flask import Flask, request
from threading import Thread

app = Flask(__name__)
sensor_value = None

@app.route("/", methods=['POST'])
def pebble():
    print request.data
    return ""

# Get sensor data and send it to timeline
def sensor():
    from random import randint
    from time import sleep
    import datetime
    delay = datetime.timedelta(hours=1).total_seconds()
    #timedelta(weeks=40, days=84, hours=23, minutes=50, seconds=600)
    while True:
        # fake sensor
        sensor_value = randint(0,25)
        subtitle = "Value = {}C".format(sensor_value)
        body = "The garage temperature is now at {}C".format(sensor_value)
        pin1 = PinCreator("Sensor Data", subtitle, body)
        #pin1.addNotification("New Data")
        pin1.display()
        pin1.send()
        print "sensor value = "+str(sensor_value)
        sleep(delay)


thread_sensor = Thread(target=sensor)
thread_sensor.setDaemon(True)
thread_sensor.start() 
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)#, debug=True)