"""
Dude! Since when has navigating the terminal using escape codes ever been 
this cool?!
"""

import time

print("Loading...", end="", flush=True)
time.sleep(1)

# Move back to start of line and overwrite
print("\rDone!     ")  # Extra spaces to clear the "..."

# Or move up and overwrite previous lines
print("Line 1")
print("Line 2")
time.sleep(1)
print("\x1B[A\rLine 2 MODIFIED")  # Up one line, return to start, overwrite
time.sleep(1)

print("\033[32;1;4mTHIS IS SICK!\033[0m")
time.sleep(1)