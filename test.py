import sys
import time
from collections import deque

queue = deque([], 3)
t = 0
while True:
    time.sleep(0.5)
    if t <= 20:
        s = "update %d" % t
        t += 1
    else:
        s = None
    for _ in range(len(queue)):
        sys.stdout.write("\x1b[1A\x1b[2K")  # move up cursor and delete whole line
    if s != None:
        queue.append(s)
    else:
        queue.popleft()
    if len(queue) == 0:
        break
    for i in range(len(queue)):
        sys.stdout.write(queue[i] + "\n")  # reprint the lines
