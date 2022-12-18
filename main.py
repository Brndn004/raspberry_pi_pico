"""Connect to WiFi and set the current time."""
import time

import onboard_led_lib
import wifi_connection_utils
import time_utils


wlan = wifi_connection_utils.get_wlan()
time_is_set = False

while True:
    wifi_connection_utils.ensure_connection(wlan)
    if not time_is_set:
        time_is_set = time_utils.set_time_via_internet()
    print(time_utils.get_time())
    if time_utils.time_matches_now(21, 1):
        onboard_led_lib.blink_sos()
    onboard_led_lib.heart_beat()
    time.sleep(1)
