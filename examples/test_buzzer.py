import time

import RPi.GPIO as GPIO


# GPIO.setmode(GPIO.BOARD)
# PIN_A = 31

try:
    PIN_A = 6
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_A, GPIO.OUT)
    GPIO.output(PIN_A,1)

    print "Programm wird mit STRG+C beendet"
    state = 1
    while True:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_A, GPIO.OUT)
        GPIO.output(PIN_A, state)

        if state == 1:
            state = 0
        else:
            state = 1
        print(state)
        time.sleep(0.6)
        GPIO.cleanup()
except KeyboardInterrupt:
     GPIO.cleanup()
