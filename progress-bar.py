import time
import timeit
import sys
import termios
import fcntl
import struct
import os

log_lines = []

def get_window_size():
  """
  Returns the window size
  
  Returns
  -------
  cr[0] : int
    number of rows
  cr[1] : int
    number of cols
  """
  cr = struct.unpack("hh", fcntl.ioctl(1, termios.TIOCGWINSZ, "1234"))
  return int(cr[0]), int(cr[1])

LOG_CAP = get_window_size()[0] - 1

def progress_bar(current, total, pipe_char="#", empty_char=".", bar_total=None):
  """
  Prints the current state of the progress bar.
  
  Parameters
  ----------
  current : int
    Current number of the step.
  total : int
    Total number of steps.
  pipe_char : str, optional
    Character used to indicate completed progress (default is "#").
  empty_char : str, optional
    Character used to indicate remaining progress (default is ".").
  bar_total : int, optional
    Total length of the progress bar. If None, adapts to terminal width.
  """

  global log_lines

  if not bar_total:
    bar_total = get_window_size()[1] - 7

  infotext = f"\x1b[38;5;226mINFO\x1b[0m: Processing step {current}\n"
  if len(log_lines) < LOG_CAP:
    log_lines.append(infotext)
    sys.stdout.write("\x1b[0K")
    sys.stdout.write(infotext)
  else:
    log_lines = log_lines[1:] + [infotext]
    sys.stdout.write("\x1b[H")
    for line in log_lines:
      sys.stdout.write(line)

  # save current cursor pos, then put cursor at bottom line
  # print progress-bar, then put cursor back to saved pos
  sys.stdout.write("\x1b[s")
  sys.stdout.write(f"\x1b[{get_window_size()[0]};0H")

  s = "["
  perc_done = int(current * 100 / total)
  num_bars = int(perc_done * bar_total / 100)
  for i in range(0, num_bars):
    s += pipe_char 
  for i in range(num_bars, bar_total):
    s += empty_char 
  s += f"] {perc_done}%"
  # print(s, end ="", flush=True)
  sys.stdout.write(s)

  # finished
  if perc_done == 100:
    sys.stdout.write("\n")
    input("Press any key to continue...")

  sys.stdout.write("\x1b[u")

def init():
  sys.stdout.write("\x1b[?1049h")
  sys.stdout.write("\x1b[2J")
  sys.stdout.write("\x1b[H")

if __name__ == "__main__":
  tstart = timeit.default_timer()
  current = 1
  total = 50
  init()
  for i in range(current, total + 1):
    progress_bar(i, total)
    time.sleep(0.05)
  sys.stdout.write("\x1b[?1049l")
  tend = timeit.default_timer()
  t = tend - tstart
  sys.stdout.write(f"\x1b[38;5;226mINFO\x1b[0m: Successfuly finished all {total} steps in {t:.2f}s\n")
