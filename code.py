"""PIM551 command deck for the TESmart DKS203-M24.

Current desk orientation: keypad on the left, Pico W on the right, with the USB
cable exiting upward. PMK's column-oriented numbering is remapped so the
finger-indicated top-left key is PC1 and commands read normally across each row.

Production boot.py must expose only one boot-protocol keyboard HID.
"""

import time
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
from tesmart_commands import (
    COMMAND_KEY_NAMES,
    COMMAND_NAMES,
    KEY_COLOURS,
    PHYSICAL_TO_LOGICAL,
    PREFIX_NAMES,
    validate_mapping,
)


DIAGNOSTIC_MODE = False
FIRMWARE_VERSION = "1.0.0"

KEY_HOLD_SECONDS = 0.10
KEY_GAP_SECONDS = 0.22
PREFIX_GAP_SECONDS = 0.30
IDLE_BRIGHTNESS_DIVISOR = 4

validate_mapping()


def resolve_key_names(names):
    return tuple(getattr(Keycode, name) for name in names)


PREFIX = resolve_key_names(PREFIX_NAMES)
COMMANDS = {
    command_name: resolve_key_names(key_names)
    for command_name, key_names in COMMAND_KEY_NAMES.items()
}

pmk = PMK(Hardware())
pmk.rotate(270)
keys = pmk.keys
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)


# Remap PMK's column-oriented numbering so the finger-indicated top-left key is
# logical position zero (PC1), followed left-to-right and top-to-bottom.
def logical_index(key):
    return PHYSICAL_TO_LOGICAL[key.number]


def restore_key_colour(key):
    colour = KEY_COLOURS[logical_index(key)]
    key.set_led(
        colour[0] // IDLE_BRIGHTNESS_DIVISOR,
        colour[1] // IDLE_BRIGHTNESS_DIVISOR,
        colour[2] // IDLE_BRIGHTNESS_DIVISOR,
    )


def tap_sequence(sequence):
    """Send separate key taps with KVM-friendly timing."""
    for keycode in sequence:
        keyboard.press(keycode)
        time.sleep(KEY_HOLD_SECONDS)
        keyboard.release_all()
        time.sleep(KEY_GAP_SECONDS)


def send_command(command_name):
    """Type a safe diagnostic label or send one documented TESmart command."""
    if DIAGNOSTIC_MODE:
        keyboard_layout.write("[{}] ".format(command_name))
        return

    if command_name == "FOCUS":
        tap_sequence(COMMANDS[command_name])
        return

    tap_sequence(PREFIX)
    time.sleep(PREFIX_GAP_SECONDS)
    tap_sequence(COMMANDS[command_name])


for key in keys:
    restore_key_colour(key)


for key in keys:
    @pmk.on_press(key)
    def press_handler(pressed_key):
        index = logical_index(pressed_key)
        command_name = COMMAND_NAMES[index]
        pressed_key.set_led(255, 255, 255)
        try:
            send_command(command_name)
            pressed_key.set_led(0, 255, 40)
        except Exception as error:
            keyboard.release_all()
            pressed_key.set_led(255, 0, 0)
            print("Command error:", command_name, error)
        time.sleep(0.12)
        restore_key_colour(pressed_key)


print("Pico RGB Command Deck v{} ready".format(FIRMWARE_VERSION))
print("Orientation: keypad left, Pico right, USB cable upward")
print("Layout:", COMMAND_NAMES)

while True:
    pmk.update()
