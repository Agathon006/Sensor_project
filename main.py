# Python code for connecting Arduino to Python
# That's Engineering
# 29/04/2020
import asyncio
import random
from typing import List, Any

import serial
import schedule


def get_sensor_data():
    # arduino = serial.Serial('com3', 115200)
    # print('Established serial connection to Arduino')
    # arduino_data = arduino.readline()
    #
    # decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    # list_values = decoded_values.split('x')

    list_in_floats = random.uniform(0, 320.2)

    # for item in list_values:
    #     list_in_floats.append(float(item))

    print(f'Collected readings from Arduino: {list_in_floats} cm')
    # await asyncio.sleep(0.5)

    arduino_data = 0
    # list_in_floats.clear()
    # list_values.clear()
    # arduino.close()
    print('Connection closed')
    print('<----------------------------->')
    return list_in_floats


# # ----------------------------------------Main Code------------------------------------
# async def main_func():
#     # Declare variables to be used
#
#     print('Program started')
#
#     # Setting up the Arduino
#     schedule.every(10).seconds.do(get_sensor_data)
#
#     while True:
#         schedule.run_pending()
#         await asyncio.sleep(1)
