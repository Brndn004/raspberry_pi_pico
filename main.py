"""Connect to WiFi and set the current time."""
import time

import onboard_led_lib
import pwm_utils
import time_utils
import wifi_connection_utils


pwm_led = pwm_utils.create_pin_for_pwm(0)
sleep_time = 1e-4
time_is_set = False
wlan = wifi_connection_utils.get_wlan()

while True:
    if not time_is_set:
        # Only check wifi if we haven't set time since that's the only reason we need it.
        wifi_connection_utils.ensure_connection(wlan)
        time_is_set = time_utils.set_time_via_internet()
    print(time_utils.get_time())
    if time_is_set and time_utils.time_matches_now(6, 10):  # No way I regret this.
        pwm_utils.fade_pwm(pwm_led, 5*60, 0, 100)  # 5 minute fade-in time.
    onboard_led_lib.heart_beat()
    time.sleep(1)
