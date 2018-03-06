import pantiltlib
import time
import numpy as np

def f(x):
#  print(x)
  return x


r1 = np.arange(0,90,1)[::-1]
r2 = np.arange(0,40,1)

for p in r1:
  pantiltlib.do_tilt(None, p)
  time.sleep(0.05)

for p in r2:
  pantiltlib.do_tilt(None, p)
  time.sleep(0.05)

while True: 
  scan_results = pantiltlib.pan_scan(f)
  print(scan_results)
  time.sleep

  scan_results = pantiltlib.pan_scan(f)
  print(scan_results)

  time.sleep(180)
