#!/usr/bin/env python

import colorsys
import math
import time
import pantilthat
import numpy as np


pantilthat.light_mode(pantilthat.WS2812)
pantilthat.light_type(pantilthat.GRBW)

pantilthat.pan(0)
pantilthat.tilt(0)
old_pan=0
old_tilt=0


def flash_lights():
    t = time.time()
    r, g, b = [int(x*255) for x in  colorsys.hsv_to_rgb(((t*100) % 360) / 360.0, 1.0, 1.0)]
    pantilthat.set_all(r, g, b)
    pantilthat.show()

def mkrange(start, stop, step):
    if start > stop:
      return np.arange(start, stop, step)[::-1]
    else:
      return np.arange(start, stop, step)

def do_pan(old, new):
    # steps = mkrange(new, old, 1) if( old > new) else mkrange(old, new, 1)
    #steps = mkrange(old, new, 20) 
    #print("old, new: ", old, new)
    #print("pan steps: ", steps)
    pantilthat.pan(new)
    old_pan = new

    #for i in steps:
    #    print("moving pan degree to: ", i) 
    #    pantilthat.pan(i)
    #    time.sleep(0.02)


def do_tilt(old, new):
    # steps = mkrange(new, old, 2) if( old > new) else mkrange(old, new, 1)
    # steps = mkrange(old, new, 1) 
    # print(steps)
    pantilthat.tilt(new)
    old_tilt = new 

    #for i in steps:
    #    print(i) 
    #    pantilthat.tilt(i)
    #    time.sleep(0.02)

def pan_scan_step(pos, f):
    pantilthat.pan(pos)
    flash_lights()
    ret = f(pos)
    return ret

def pan_scan(f):
  pantilthat.pan(-90)
  positions = mkrange(-90,90,10)
  print(positions)
  result = []
  for pos in positions:
    result.append(pan_scan_step(pos, f))
    time.sleep(0.1)

  rev_positions = mkrange(90, 0, 10)
  print(rev_positions)

  for pos in rev_positions:
    result.append(pan_scan_step(pos, f))
    time.sleep(0.1)

  return result
  
  
def tilt_dance():
  r1 = mkrange(90,0,2)
  r2 = mkrange(0,40,2)

  for p in r1:
    do_tilt(None, p)
    time.sleep(0.05)

  for p in r2:
    do_tilt(None, p)
    time.sleep(0.05)


def move_camera(new_pan, new_tilt):
    global old_pan
    global old_tilt

    print(old_pan, new_pan)
    flash_lights()

    # emulate pan_amount as input
    new_pan = old_pan + new_pan
    do_pan(old_pan, new_pan)
    old_pan = new_pan
    #do_tilt(old_tilt, tilt_amount)
    # old_tilt = tilt_amount
    flash_lights()

#move_camera(10, None)

#while True:
#    t = time.time()
#    b = (math.sin(t * 2) + 1) / 2
#    b = int(b * 255.0)
#    t = round(time.time() * 1000) / 1000
#    a = int(round(math.sin(t) * 90))
#    do_tilt(old_tilt, a)
#    old_tilt = a
#    print("done with: ", a)
#    print(a)
#    time.sleep(1)
