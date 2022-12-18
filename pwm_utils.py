"""Util functions for pulse-width-modulation (PWM)."""
import machine
import utime

_PWM_PIN_SET_EXECUTION_TIME = 9.536048e-06


def create_pin_for_pwm(desired_pin: int) -> machine.PWM:
    """Create a pin for pulse-width modulation and set it to zero output."""
    pwm_pin = machine.PWM(machine.Pin(desired_pin))
    pwm_pin.freq(100)  # 100 Hz
    pwm_pin.duty_u16(0)
    return pwm_pin


def percent_to_duty_u16(pct_desired: int):
    """Desired percent is a value in [0, 100]."""
    pct_clamped_norm = min(1, max(0, pct_desired / 100.0))
    return int(65535 * pct_clamped_norm)


def set_pwm_pct(pwm_pin: machine.PWM, pct_desired: int) -> None:
    """Set a PWM pin to a specific percent."""
    pwm_pin.duty_u16(percent_to_duty_u16(pct_desired))


def fade_pwm(pwm_pin: machine.PWM, duration_sec: float, start_pct: int, end_pct: int) -> None:
    """Fade from start % to end % over a specific period of time.

    start_pct < end_pct is a fade in.
    start_pct > end_pct is a fade out.
    start_pct = end_pct will not have any effect at all.

    Args:
        pwm_pin: The pin that you want to fade in.
        duration_sec: How long you want the fade in to last in seconds.
        start_pct: The percent at which the fade should start. Should be in [0, 100].
        end_pct: The percent at which the fade should end. Should be in [0, 100].
    """
    # Set loop variables.
    start_duty = percent_to_duty_u16(start_pct)
    end_duty = percent_to_duty_u16(end_pct)
    step_size = 1 if start_duty < end_duty else -1

    # Compute sleep time.
    num_steps = abs((end_duty - start_duty) / step_size)  # Break out for clarity.
    pwm_pin_set_execution_time_sec = _PWM_PIN_SET_EXECUTION_TIME * num_steps
    total_sleep_duration = duration_sec - pwm_pin_set_execution_time_sec
    sleep_time = int(total_sleep_duration / num_steps * 1e6)  # Microseconds.

    for duty in range(start_duty, end_duty, step_size):
        pwm_pin.duty_u16(duty)
        utime.sleep_us(sleep_time)


def fade_in_and_out(pwm_pin: machine.PWM, duration_sec: float) -> None:
    """Tell a PWM pin to fade in and out over the specified duration."""
    fade_pwm(pwm_pin, duration_sec / 2, 0, 100)
    fade_pwm(pwm_pin, duration_sec / 2, 100, 0)
