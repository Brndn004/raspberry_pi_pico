from machine import Pin

onboard_led = Pin("LED", Pin.OUT)

def toggle_onboard_led():
  onboard_led.toggle()
