"""Wifi- and networking-related functionality."""
import network
import time
import urequests

import onboard_led_lib


SSID: str = "probablymalicious"
PW: str = "installavirusnow"


def get_wlan() -> network.WLAN:
    """Returns a WLAN object so we don"t have to check for None everywhere."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan


def _connect_wlan(wlan: network.WLAN) -> None:
    """Connects to my hard-coded WiFi network."""
    print(f"Connecting to {SSID}.")
    wlan.connect(SSID, PW)
    remaining_wait_time = 10
    while remaining_wait_time > 0 and not (wlan.status() < 0 or wlan.status() >= 3):
        remaining_wait_time -= 1  # Probably an off-by-one error.
        print(f"Waiting {remaining_wait_time} more seconds for a connection...")
        time.sleep(1)
    if wlan.status() == 3:
        print("Connection successful.")
    else:
        print("Failed to connect in time.")


def _cycle_wlan(wlan: network.WLAN) -> None:
    """Connect to WiFi using an existing WLAN object."""
    print("Cycling wlan object.")
    wlan.disconnect()
    _connect_wlan(wlan)


def _can_access_internet(wlan: network.WLAN) -> bool:
    """Queries a simple server as a litmus test for being able to access the internet."""
    try:
        resp = urequests.get("http://date.jsontest.com")
        resp.close()
        return True
    except Exception:  # Too general on purpose since I don't care what the error is.
        return False


def ensure_connection(wlan: network.WLAN) -> None:
    """Connects to wifi, if needed.

    Args:
        wlan: If wlan is a valid object, then this function checks
            the connection status and attempts a reconnection if needed.
    """
    if not wlan.isconnected() or not _can_access_internet(wlan):
        onboard_led_lib.blink_sos()
        _cycle_wlan(wlan)
    if not wlan.isconnected():
        onboard_led_lib.display_error_until_next_command()
