"""Test out simple pico functionality."""
import time
import onboard_led_lib

SLEEP_TIME_SEC = 0.5

while True:
    onboard_led_lib.toggle_onboard_led()
    time.sleep(SLEEP_TIME_SEC)
