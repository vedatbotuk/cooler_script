#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from os import popen

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

IMPULS_PIN_HIGH = 21  # Pin, der zum Transistor fuehrt
IMPULS_PIN_LOW = 19
SLEEP_TIME = 2  # Alle wie viel Sekunden die Temperatur ueberprueft wird
# FUN_TIME		= 30
fan_high = 55  # Ab welcher CPU Temperatur der Luefter sich drehen soll
fan_low = 45

starter = 0


def get_cpu_temperature():
    temp = str(popen('vcgencmd measure_temp').readline())
    return float(temp.replace("temp=", "").replace("'C\n", ""))


def fan_high_on():
    GPIO.output(IMPULS_PIN_HIGH, True)
    sleep(SLEEP_TIME)


def fan_high_off():
    GPIO.output(IMPULS_PIN_HIGH, False)


def fan_low_on():
    GPIO.output(IMPULS_PIN_HIGH, True)
    sleep(1)
    GPIO.output(IMPULS_PIN_HIGH, False)
    GPIO.output(IMPULS_PIN_LOW, True)
    sleep(SLEEP_TIME)


def fan_low_off():
    GPIO.output(IMPULS_PIN_LOW, False)


# def fan_low_starter():
#     GPIO.output(IMPULS_PIN_HIGH, True)
#     sleep(0.5)
#     fan_high_off()
#     fan_low_on()


def main():
    global starter
    GPIO.setup(IMPULS_PIN_HIGH, GPIO.OUT)
    GPIO.setup(IMPULS_PIN_LOW, GPIO.OUT)
    GPIO.output(IMPULS_PIN_HIGH, False)
    GPIO.output(IMPULS_PIN_LOW, False)

    fan_high_on()
    sleep(5)
    fan_high_off()

    while True:
        sleep(1)
        cpu_temp = get_cpu_temperature()

        if cpu_temp < fan_low:
            fan_low_off()
            fan_high_off()
            starter = 0

        if starter == 0:
            if (cpu_temp >= fan_low) and (cpu_temp < fan_high):
                fan_high_off()
                fan_low_on()
                starter = 1

        if cpu_temp >= fan_high:
            fan_low_off()
            fan_high_on()


try:
    main()

except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    GPIO.output(IMPULS_PIN_HIGH, False)
    GPIO.output(IMPULS_PIN_LOW, False)
    GPIO.cleanup()  # resets all GPIO ports used by this program
