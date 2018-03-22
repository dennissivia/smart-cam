#!/usr/bin/env python

import colorsys
import math
import time
import pantilthat
import numpy as np


pantilthat.light_mode(pantilthat.WS2812)
pantilthat.light_type(pantilthat.GRBW)

pantilthat.pan(0)
pantilthat.tilt(40)
old_pan=0
old_tilt=40


def flash_lights():
    t = time.time()
    r, g, b = [int(x*255) for x in  colorsys.hsv_to_rgb(((t*100) % 360) / 360.0, 1.0, 1.0)]
    r, g, b = (255,255,255)
    for i in range(2,6):
        pantilthat.set_pixel(i, r, g, b)
    pantilthat.show()

def color_to_rgb(color):
  # print("color requested: ", color)
  if color == "red":
    return (255,0,0)
  elif color == "green":
    return (0,255,0)
  elif color == "blue":
    return (0,0,255)
  elif color == "yellow":
    return (255,255,0)
  elif color == "white":
    return (255,255,255)
  elif color == "rose":
    return (255,192,203)
  elif color == "pink":
    return (255,20,147)
  elif color == "off":
    return (0,0,0)
  else:
    return (0,0,0)

def set_light_color(color, indices=None):
    (r,g,b) = color_to_rgb(color)
    # print("rgb requested: ", (r,g,b))
    if indices is None:
        pantilthat.set_all(r,g,b)
    else:
        for idx in indices:
            pantilthat.set_pixel(idx, r,g,b)
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
  positions = mkrange(-90,90,15)

  # move to the first position without invoking the callback
  # this makes sure we dont get a camera info during the move
  pantilthat.pan(positions[0])
  time.sleep(0.5)

  # print(positions)
  result = []
  for pos in positions:
    result.append(pan_scan_step(pos, f))
    time.sleep(0.2)

  rev_positions = mkrange(90, 0, 15)
  # print(rev_positions)

  for pos in rev_positions:
    result.append(pan_scan_step(pos, f))
    time.sleep(0.2)
  return result


def tilt_dance():
  r1 = mkrange(90,0,5)
  r2 = mkrange(0,40,5)

  for p in r1:
    do_tilt(None, p)
    time.sleep(0.2)

  for p in r2:
    do_tilt(None, p)
    time.sleep(0.2)


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

