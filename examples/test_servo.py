import RPi.GPIO as GPIO
from servo import trigger_servo 

try:
  servoPIN = 26
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(servoPIN, GPIO.OUT)

  p = GPIO.PWM(servoPIN, 50) # GPIO 17 als PWM mit 50Hz
  p.start(2.5) # Initialisierung

  while True:
    trigger_servo(p)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
