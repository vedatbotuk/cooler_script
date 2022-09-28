#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from os import popen

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN_STRONG_FAN = 21  # Pin, der zum Transistor fuehrt
PIN_LIGHT_FAN = 19
SLEEP_TIME = 2  # Alle wie viel Sekunden die Temperatur ueberprueft wird

STRONG_FAN = 55  # Ab welcher CPU Temperatur der Luefter sich drehen soll
LIGHT_FAN = 45

STARTER = 0


def get_cpu_temperature():
    temp = str(popen('vcgencmd measure_temp').readline())
    return float(temp.replace("temp=", "").replace("'C\n", ""))


def fan_high_on():
    GPIO.output(PIN_STRONG_FAN, True)
    sleep(SLEEP_TIME)


def fan_high_off():
    GPIO.output(PIN_STRONG_FAN, False)


def fan_low_on():
    GPIO.output(PIN_STRONG_FAN, True)
    sleep(1)
    GPIO.output(PIN_STRONG_FAN, False)
    GPIO.output(PIN_LIGHT_FAN, True)
    sleep(SLEEP_TIME)


def fan_low_off():
    GPIO.output(PIN_LIGHT_FAN, False)


def main():
    global STARTER
    GPIO.setup(PIN_STRONG_FAN, GPIO.OUT)
    GPIO.setup(PIN_LIGHT_FAN, GPIO.OUT)
    GPIO.output(PIN_STRONG_FAN, False)
    GPIO.output(PIN_LIGHT_FAN, False)

    fan_high_on()
    sleep(5)
    fan_high_off()

    while True:
        sleep(1)
        cpu_temp = get_cpu_temperature()

        if cpu_temp < LIGHT_FAN:
            fan_low_off()
            fan_high_off()
            STARTER = 0

        if STARTER == 0:
            if (cpu_temp >= LIGHT_FAN) and (cpu_temp < STRONG_FAN):
                fan_high_off()
                fan_low_on()
                STARTER = 1

        if cpu_temp >= STRONG_FAN:
            fan_low_off()
            fan_high_on()


try:
    main()

except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    GPIO.output(PIN_STRONG_FAN, False)
    GPIO.output(PIN_LIGHT_FAN, False)
    GPIO.cleanup()  # resets all GPIO ports used by this program
