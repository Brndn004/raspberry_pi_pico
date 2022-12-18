"""Util functions for pulse-width-modulation (PWM)."""


def percent_to_duty_u16(percent_desired_norm):
    """Desired percent is a normalized value in [0, 1]"""
    pct_clamped = min(1, max(0, percent_desired_norm))
    return int(65535 * pct_clamped)
