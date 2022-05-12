# Python code for connecting Arduino to Python
# That's Engineering
# 29/04/2020
import threading

import serial
import time
import schedule


def main_func():
    arduino = serial.Serial('com3', 115200)
    print('Established serial connection to Arduino')
    arduino_data = arduino.readline()

    list_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    #list_values = decoded_values.split('x')

    for item in list_values:
        list_in_floats.append(float(item))

    print(f'Collected readings from Arduino: {list_in_floats} cm')

    arduino_data = 0
    list_in_floats.clear()
    list_values.clear()
    arduino.close()
    print('Connection closed')
    print('<----------------------------->')


# ----------------------------------------Main Code------------------------------------
# Declare variables to be used
list_values = []
list_in_floats = []

print('Program started')

# Setting up the Arduino
schedule.every(1).seconds.do(main_func)

while True:
    schedule.run_pending()
    time.sleep(1)
