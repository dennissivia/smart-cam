import pantiltlib
import time
import sys
import RPi.GPIO as GPIO
import Adafruit_DHT
from RPLCD.i2c import CharLCD
from identify_user import identify


absolute_center = 1240.0 / 2.0
projection_factor = absolute_center / 26.0

def f(x):
  #print(x)
  return x

def identify_and_track():
  print("start")
  val = identify()
  print("stop")
  if val != None:
    print("found face. adjusting camera")
    amount = val - absolute_center
    degree = amount / projection_factor
    print("DEBUG current val, amount, degree: ") 
    print("DEBUG", val, amount, degree)
    if abs(amount) > 100:
      print("adjustment of more than 100 needed")
      if amount < 0:
        pantiltlib.move_camera(-1 * degree, None)
      else:
        pantiltlib.move_camera(-1 * degree, None)

# -------------------

def print_move_count(n):
    #lcd.clear()
    #lcd.cursor_pos = (0, 0)
    #lcd.write_string("Moves: %d" % n)
    print("Moves: %d" % n)
    return None

def print_motion_detected(n):
    #lcd.clear()
    #lcd.cursor_pos = (0, 0)
    #lcd.write_string("Motion detected!")
    #lcd.cursor_pos = (1, 0)
    #lcd.write_string("Moves: %d" % n)
    print("Motion detected!")

    time.sleep(1)
    print("Moves: %d" % n)
    return None

def toggleLED(channel, onoff):
    GPIO.output(channel, onoff)
 
def get_control_state():
    state = int(GPIO.input(CTRL_LED_PIN))
    return state

def pan_scan_callback(pos):
  print("starting")
  val = identify()
  print("stopping")
  if val != None:
    return pos
  else:
    return None

def camera_scan_on_motion():
    print("motion detected. strting scan")
    scan_results = pantiltlib.pan_scan(pan_scan_callback)
    print(scan_results)
    position = list(filter(lambda x: x != None, scan_results))[0]
    if position: 
        print("selecting position: ", position)
        pantiltlib.do_pan(None, position)
        for i in range(6):
            print("tracking iteration: ",i)
            identify_and_track()

def callback(channel):
    state = get_control_state()
    global global_move_count
    print('Motion detected!')
    if state == 1:
        print('Switching on LEDs.')
        toggleLED(LED_PIN, True)

        camera_scan_on_motion()
        time.sleep(2)

        print('Turning off again.')
        toggleLED(LED_PIN, False)
        global_move_count += 1
        print_motion_detected(global_move_count)
    else:
        print('ignoring event. Control state is: ', state)


#lcd = CharLCD("PCF8574", 0x64)
global_move_count = 0

GPIO.setmode(GPIO.BCM)

# motion detector
SENSOR_PIN = 12
GPIO.setup(SENSOR_PIN, GPIO.IN)

CTRL_LED_PIN = 16
GPIO.setup(CTRL_LED_PIN, GPIO.OUT)

initial_button_state = 1
print("initial button state: ", initial_button_state)
GPIO.output(CTRL_LED_PIN, initial_button_state == 1)

LED_PIN = 26
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, False)

try: 
    # lcd --------
    #lcd.clear()
    #lcd.home()
    #lcd.write_string("Welcome :)")
    # ----------
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=callback)

    pantiltlib.tilt_dance()

    while True:
        camera_scan_on_motion()
        print_move_count(global_move_count)
        time.sleep(20.0)

except KeyboardInterrupt:
    print("Done...")

finally:
    GPIO.cleanup()
    #lcd.close(clear=True)
