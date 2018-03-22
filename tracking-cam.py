import pantiltlib
import time
import sys
import RPi.GPIO as GPIO
import Adafruit_DHT
from RPLCD.i2c import CharLCD
import nfc
from nfc.clf import RemoteTarget
#from identify_user import identify
from object_detector import detect
from threading import Thread



absolute_center = 1024.0 / 2.0
projection_factor = absolute_center / 26.0
scan_in_progress = False
scan_pending = False
global_move_count = 0
global_program_ending = False
last_scan_time = -1


# lcd = None
nfc_thread = None
lcd = CharLCD("PCF8574", 0x3f, port=1)
clf = nfc.ContactlessFrontend()
CTRL_PIXELS=(0,1)
FACE_PIXELS=(2,3,4,5)
MOVE_PIXELS=(6,7)


def current_timestamp():
    return int(round(time.time()))

def f(x):
  return x

def init_display():
  if lcd is not None:
    lcd.clear()
    lcd.home()

def display(s, row=0):
  if lcd is not None:
    lcd.cursor_pos = (row, 0)
    lcd.write_string(s)

def close_display():
  if lcd is not None:
    lcd.close(clear=True)

def identify():
    return detect()

def register_scan():
    print("STATE: scan_in_progress: scan got registered")
    global scan_in_progress
    scan_in_progress = True

def unregister_scan():
    print("STATE: scan_in_progress => False: scan got unregistered")
    global scan_in_progress
    global last_scan_time
    last_scan_time = current_timestamp()
    scan_in_progress = False

def extract_first_person(objects):
    people = filter(lambda (l,p): l == 'person', objects)
    if len(people) > 0:
        return people[0]
    else:
        return None

def identify_and_adjust():
  pantiltlib.set_light_color("off",FACE_PIXELS)
  objects = identify()
  if objects is not None:
      print(objects)
      person = extract_first_person(objects)
      if person is not None:
          (label, center) = person
          print("face detected. Making stuff Pink now.")
          display("Face detected",row=1)
          pantiltlib.set_light_color("pink",FACE_PIXELS)
          time.sleep(4)
          amount = center - absolute_center
          degree = amount / projection_factor
          # print("DEBUG detected center, amount, degree: ")
          # print("DEBUG", center, amount, degree)
          if abs(amount) > 60:
              print("mismatch of more than 60px detected. adjustment needed.")
              if amount < 0:
                  pantiltlib.move_camera(-1 * degree, None)
              else:
                  pantiltlib.move_camera(-1 * degree, None)

# -------------------

def print_move_count(n):
    if lcd is not None:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Moves: %d" % n)
    else:
        print("Moves: %d" % n)
    return None

def print_motion_detected(n):
    if lcd is not None:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Motion detected!")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Moves: %d" % n)
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
  objects = identify()
  # print(objects)
  if objects is not None:
    person = extract_first_person(objects)
    if person is not None:
      return pos
    else:
      return None
  else:
    return None

def track_person():
    print("performing 10 tracking steps now")
    for i in range(10):
        identify_and_adjust()

def buzzer_alert():
    for i in range(3):
        GPIO.output(BUZZER_PIN, 1)
	time.sleep(0.2)
        GPIO.output(BUZZER_PIN, 0)
	time.sleep(0.2)


def camera_scan_on_motion():
    register_scan()
    print("Starting scan")
    scan_results = pantiltlib.pan_scan(pan_scan_callback)
    print(scan_results)
    positions = list(filter(lambda x: x != None, scan_results))
    if not positions:
        print("no face detected")
    else:
        position = positions[0]
        print("Person detected. Alert and tracking initiated.")
	buzzer_alert()
        # print("selecting position: ", position)
        pantiltlib.do_pan(None, position)
        track_person()
    unregister_scan()

def read_nfc():
    target = clf.sense(RemoteTarget('106A'),RemoteTarget('106B'),RemoteTarget('212F'))
    if target is not None:
        print(target)
        tag = nfc.tag.activate(clf, target)
        print(tag)
        return tag.identifier.encode("hex").upper()
    else:
        return None

def trigger_alert_lights():
    # toggleLED(LED_PIN, True)
    pantiltlib.set_light_color("red",MOVE_PIXELS)
    time.sleep(3.0)
    pantiltlib.set_light_color("off",MOVE_PIXELS)
    # toggleLED(LED_PIN, False)


def check_nfc_tag():
    card_id = read_nfc()
    if card_id is not None:
        # card 3 or dennis google pixel phone
        if card_id == "A05481A5" or card_id == "086784DF":
            print("recognized card id: ", card_id)
            print("chaning control state")
            old_state = int(GPIO.input(CTRL_LED_PIN))
            new_state = abs(old_state - 1)
            #print("old state: ", old_state)
            #print("new state: ", new_state)
            GPIO.output(CTRL_LED_PIN, new_state)
            if new_state == 1:
                pantiltlib.set_light_color("red",CTRL_PIXELS)
            else:
                pantiltlib.set_light_color("green",CTRL_PIXELS)
        else:
            print("ignoring unknown card: ",card_id)

# We could add an argunent, like a map of arguments, like gpio object etc..
def nfc_reader_thread():
    global global_program_ending
    while global_program_ending is False:
        try:
            check_nfc_tag()
            # print("polling nfc reader")
            time.sleep(0.6)
        except:
            print("nfc reader thread failed. Ignoring all errors", sys.exc_info())
            time.sleep(10) # make sure we dont have a tight exception loop


def callback(channel):
    state = get_control_state()
    global global_move_count
    global scan_pending
    print('Motion detected!')
    if state == 1:
        trigger_alert_lights()
        global_move_count += 1
        print_motion_detected(global_move_count)
        if not scan_in_progress:
            print("currently no scan in progress ", scan_in_progress)
            scan_pending = True
        else:
            print("scan already in progress.")
    else:
        print('ignoring event. Control state is: ', state)


GPIO.setmode(GPIO.BCM)
# motion detector
SENSOR_PIN = 24
GPIO.setup(SENSOR_PIN, GPIO.IN)

CTRL_LED_PIN = 16
GPIO.setup(CTRL_LED_PIN, GPIO.OUT)

initial_button_state = 1
print("initial button state: ", initial_button_state)
GPIO.output(CTRL_LED_PIN, initial_button_state == 1)
pantiltlib.set_light_color("red",CTRL_PIXELS)


LED_PIN = 26
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, False)

# GPIO.setmode(GPIO.BOARD)
# PIN_A = 31

BUZZER_PIN = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN,0)

try:
    last_scan_time = current_timestamp()
    clf.open('tty')
    # lcd --------
    display("Welcome :)")
    time.sleep(1.0)
    # ----------
    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=callback, bouncetime=2000)

    nfc_thread = Thread(target = nfc_reader_thread)
    nfc_thread.start()

    pantiltlib.tilt_dance()

    while True:
        print_move_count(global_move_count)
        identify_and_adjust()
        print("scan pending, scan in progress: ", scan_pending, scan_in_progress)
        if scan_pending is True:
            time_since_last_scan = (current_timestamp() -  last_scan_time)
            if time_since_last_scan < 20:
                print("Last scan is less than 20s ago. deferring.")
            else:
                print("STATE: performing pending scan")
                scan_pending = False
                camera_scan_on_motion()
        time.sleep(0.5)


except KeyboardInterrupt:
    global_program_ending = True
    print("stopping additional threads...")
    nfc_thread.join()
    print("Done.")

finally:
    GPIO.cleanup()
    close_display()
    clf.close()
