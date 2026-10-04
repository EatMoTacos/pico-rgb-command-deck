"""Known-good TESmart keyboard-only USB configuration for the Pico W.

Normal boot:
    Present exactly one boot-protocol USB keyboard. This is the configuration
    verified with the TESmart DKS203-M24 CH545 keyboard/HID port, both directly
    and through the shared hub with the 8BitDo receiver.

Recovery/development boot:
    Connect GP14 (physical pin 19) to GND before powering or resetting the Pico.
    CircuitPython's normal CIRCUITPY drive and USB serial console remain enabled.

BOOTSEL remains the final UF2 recovery method.
"""

import board
import digitalio
import storage
import usb_cdc
import usb_hid
import usb_midi


# GP14 has an internal pull-up. Grounding it only during startup requests
# development mode. Never connect GP14, RUN, or GND to 3.3 V or 5 V.
recovery_pin = digitalio.DigitalInOut(board.GP14)
recovery_pin.switch_to_input(pull=digitalio.Pull.UP)
development_mode = not recovery_pin.value
recovery_pin.deinit()

if not development_mode:
    # Keep the USB identity deliberately boring for the TESmart CH545:
    # no storage, serial, MIDI, mouse, or consumer-control interfaces.
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_midi.disable()
    usb_hid.enable((usb_hid.Device.KEYBOARD,), boot_device=1)
