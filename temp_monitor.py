import os
import glob
import time
from flask import Flask, render_template

# Initialize the Flask app
app = Flask(__name__)

# Set up the 1-Wire sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
device_folder = '/sys/bus/w1/devices/28-000005e2fdc3/w1_slave'

# Function to read the temperature
def read_temperature():
    f = open(device_folder, 'r')
    lines = f.readlines()
    f.close()
    if lines[0].strip()[-3:] == 'YES':
        temp_output = lines[1].split('t=')[1]
        temperature = float(temp_output) / 1000.0
        return temperature
    else:
        return None

# Route to display the temperature on a webpage
@app.route('/')
def index():
    temperature = read_temperature()
    return render_template('index.html', temperature=temperature)

# Run the web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
