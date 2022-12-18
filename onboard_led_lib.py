import time
from machine import Pin


ONBOARD_LED = Pin("LED", Pin.OUT)


def toggle_onboard_LED():
    ONBOARD_LED.toggle()


def display_error_until_next_command() -> None:
    """Display the error signal (LED is on); overwritten if anyone commands the LED afterward."""
    ONBOARD_LED.on()


def blink_n_times(nn: int, sleep_time: float = 0.1) -> None:
    ONBOARD_LED.off()
    for _ in range(nn):
        ONBOARD_LED.on()
        time.sleep(sleep_time)
        ONBOARD_LED.off()
        time.sleep(sleep_time)


def heart_beat() -> None:
    blink_n_times(1)


def blink_sos() -> None:
    blink_n_times(3, 0.1)
    blink_n_times(3, 0.2)
    blink_n_times(3, 0.1)
