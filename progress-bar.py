import time
import sys
import termios
import fcntl
import struct
import os

def get_window_size():
  cr = struct.unpack("hh", fcntl.ioctl(1, termios.TIOCGWINSZ, "1234"))
  return int(cr[1])

def progress_bar(current, total, pipe_char="#", empty_char=".", bar_total=None):
  s = "["
  if not bar_total:
    bar_total = get_window_size() - 6 
  perc_done = int(current * 100 / total)
  num_bars = int(perc_done * bar_total / 100)
  for i in range(0, num_bars):
    s += pipe_char 
  for i in range(num_bars, bar_total):
    s += empty_char 
  s += f"] {perc_done}%"
  print(s, end ="")

if __name__ == "__main__":
  current = 1
  total = 500
  for i in range(current, total + 1):
    progress_bar(i, total)
    sys.stdout.write("\r")
    time.sleep(0.001)
    sys.stdout.write("\033[K")
