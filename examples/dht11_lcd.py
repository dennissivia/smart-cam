#!/usr/bin/python
import sys
import time
import Adafruit_DHT

#from RPLCD import CharLCD
#from RPi import GPIO
#lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23], numbering_mode=GPIO.BOARD)

from RPLCD.i2c import CharLCD
lcd = CharLCD("PCF8574", 0x3f, port=1)

try:
    lcd.clear()
    lcd.home()
    lcd.write_string("Welcome :)")
    time.sleep(3)

    while True:
        lcd.clear()
        lcd.home()
        lcd.write_string("Reading DHT11")
        time.sleep(3)

        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        if humidity > 100:
            continue
        print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)

        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Temp: %d C" % temperature)

        lcd.cursor_pos = (1, 0)
        lcd.write_string("Humidity: %d %%" % humidity)
        time.sleep(10)

finally:
    lcd.close(clear=True)
    GPIO.cleanup()

