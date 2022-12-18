import time

from machine import Pin, PWM

def percent_to_duty_u16(percent_desired_norm):
    """Desired percent is a normalized value in [0, 1]"""
    pct_clamped = min(1, max(0, percent_desired_norm))
    return int(65535 * pct_clamped)

onboard_led = Pin("LED", Pin.OUT)
mosfet_gate = PWM(Pin(0))
mosfet_gate.freq(100)
mosfet_gate.duty_u16(percent_to_duty_u16(0.5))

sleep_time = 0.0001

delta_pwm = 1
min_pwm = percent_to_duty_u16(0)
max_pwm = percent_to_duty_u16(0.1)

while True:
    for pwm_val in range(min_pwm, max_pwm, delta_pwm):
        mosfet_gate.duty_u16(pwm_val)
        time.sleep(sleep_time)
    onboard_led.toggle()
    for pwm_val in range(max_pwm, min_pwm, -delta_pwm):
        mosfet_gate.duty_u16(pwm_val)
        time.sleep(sleep_time)
    onboard_led.toggle()
