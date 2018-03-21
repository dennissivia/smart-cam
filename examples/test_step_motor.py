import RPi.GPIO as GPIO
 
from step_motor import trigger_step_motor

GPIO.setmode(GPIO.BCM)

coil_A_1_pin = 4 # pink
coil_A_2_pin = 17 # orange
coil_B_1_pin = 23 # blau
coil_B_2_pin = 24 # gelb
 
StepCount = 8
# anpassen, falls andere Sequenz
Seq = list(range(0, StepCount))
Seq[0] = [0,1,0,0]
Seq[1] = [0,1,0,1]
Seq[2] = [0,0,0,1]
Seq[3] = [1,0,0,1]
Seq[4] = [1,0,0,0]
Seq[5] = [1,0,1,0]
Seq[6] = [0,0,1,0]
Seq[7] = [0,1,1,0]
 

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
 
try: 
    pins = [coil_A_1_pin, coil_A_2_pin, coil_B_1_pin, coil_B_2_pin]
    while True:
        trigger_step_motor(10,20000,10,pins, Seq, StepCount)
finally:
  GPIO.cleanup()
