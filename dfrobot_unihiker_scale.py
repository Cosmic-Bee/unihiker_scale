#!/usr/bin/python3
import time
from unihiker import GUI
from pinpong.board import Board, I2C, Pin, NeoPixel
from pinpong.extension.unihiker import *
from dfrobot_i2c_hx711 import DFRobot_HX711_I2C
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# Weight value
CALIBRATION_WEIGHT_VALUE=50

# Arbitrary value for light sensor to trigger LED ring light
LIGHT_ENABLE_THRESHOLD = 300

Board("UNIHIKER").begin()
NEOPIXEL_PIN = Pin(22)
PIXELS_NUM = 8
neopixel = NeoPixel(NEOPIXEL_PIN, PIXELS_NUM)

# Initialize GUI and variables
gui = GUI()
lightEnabled = None
hx711_sensor = DFRobot_HX711_I2C()

# Initialize the HX711 sensor
hx711_sensor.begin()

# Page header
gui.draw_text(text="Weight Sensor", x=30, y=20, font_size=20, color="teal")
state = gui.draw_text(text="Current State: Weighing", x=30, y=80, font_size=10, color="blue")

# Weight display
weightText = gui.draw_text(text="0.00 g", x=20, y=180, font_size=34, color="teal")

def handleNightMode():
    global lightEnabled
    lightValue = light.read()
    if 0 <= lightValue < LIGHT_ENABLE_THRESHOLD:
        lightEnabled = True
        for i in range(PIXELS_NUM):
            neopixel[i] = (20, 20, 20)
    elif lightEnabled:
        lightEnabled = False
        for i in range(PIXELS_NUM):
            neopixel[i] = (0, 0, 0)

# Track the time when the state was last changed
last_state_change_time = time.time()
initial_state_set = False

while True:
    handleNightMode()

    # Check if button A is pressed for calibration
    if button_a.is_pressed() == True:
        state.config(text="Current State: Calibrating {}g".format(CALIBRATION_WEIGHT_VALUE))
        last_state_change_time = time.time()
        hx711_sensor.setTriggerWeight(CALIBRATION_WEIGHT_VALUE)
        hx711_sensor.setCalThreshold(1)
        hx711_sensor.enableCalibration()
        i = 0
        while hx711_sensor.peelFlag() != 2:
            time.sleep(1)
            i += 1
            if i >= 7:
                break
        calibration = hx711_sensor.calibration()
        state.config(text="Calibrated: {:.2f}".format(calibration))
        hx711_sensor.setCalibration(calibration)
        last_state_change_time = time.time()
        initial_state_set = False

    # Check if button B is pressed for tare (peel)
    if button_b.is_pressed() == True:
        state.config(text="Current State: Peeled")
        last_state_change_time = time.time()
        hx711_sensor.peel()
        initial_state_set = False

    # Update the weight display
    weight = hx711_sensor.weight(10)
    weightText.config(text="{:.2f} g".format(weight))

    # Check and update the state to "Current State: Weighing" if needed
    if not initial_state_set and (time.time() - last_state_change_time) >= 5:
        state.config(text="Current State: Weighing")
        initial_state_set = True

    time.sleep(0.1)
