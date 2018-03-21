import RPi.GPIO as GPIO
import time
 
def setStep(pins, ws):
  for i in range(len(pins)):
    GPIO.output(pins[i], ws[i])
        
 
def forward(delay, steps, pins, Seq, StepCount):
    for i in range(steps):
        for j in range(StepCount):
            setStep(pins, [Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3]])
            time.sleep(delay)
 
def backwards(delay, steps, pins, Seq, StepCount):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(pins, [Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3]])
            time.sleep(delay)
            

def trigger_step_motor(delay,forward_steps, backward_steps, pins, Seq, StepCount):
  steps1 = forward_steps
  steps2 = backward_steps
  forward(int(delay) / 1000.0, int(steps1), pins, Seq, StepCount)
  backwards(int(delay) / 1000.0, int(steps2), pins, Seq, StepCount)
