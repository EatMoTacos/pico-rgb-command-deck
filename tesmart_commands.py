"""Pure TESmart key-map and RGB data shared by firmware and local tests."""

COMMAND_NAMES = (
    "PC1", "PC2", "MON1", "MON2",
    "MON3", "FOCUS", "FOLLOW", "USB_AUDIO",
    "HID_MODE", "NETWORK", "EDID", "BUZZER",
    "LIGHTS_OFF", "LIGHTS_LINKED", "LIGHTS_MARQUEE", "LIGHTS_BREATHE",
)

# Symbolic key names are resolved to adafruit_hid.keycode.Keycode in code.py.
# TESmart uses the unshifted physical backtick/grave-accent key twice.
PREFIX_NAMES = ("GRAVE_ACCENT", "GRAVE_ACCENT")
COMMAND_KEY_NAMES = {
    "PC1": ("ONE",),
    "PC2": ("TWO",),
    "MON1": ("LEFT_ARROW",),
    "MON2": ("DOWN_ARROW",),
    "MON3": ("RIGHT_ARROW",),
    "FOCUS": ("RIGHT_ALT", "RIGHT_ALT"),
    "FOLLOW": ("GRAVE_ACCENT",),
    "USB_AUDIO": ("ZERO",),
    "HID_MODE": ("F2",),
    "NETWORK": ("F4",),
    "EDID": ("F5",),
    "BUZZER": ("F11",),
    "LIGHTS_OFF": ("L", "ZERO"),
    "LIGHTS_LINKED": ("L", "ONE"),
    "LIGHTS_MARQUEE": ("L", "TWO"),
    "LIGHTS_BREATHE": ("L", "THREE"),
}

# PC=blue, monitors=red, routing/USB=green, settings=amber. The lighting row
# uses its original four static colours and does not animate locally.
KEY_COLOURS = (
    (0, 90, 255), (0, 90, 255),
    (255, 25, 20), (255, 25, 20), (255, 25, 20),
    (0, 220, 100), (0, 220, 100), (0, 220, 100),
    (255, 145, 0), (255, 145, 0), (255, 145, 0), (255, 145, 0),
    (30, 30, 30), (160, 0, 255), (255, 0, 120), (255, 70, 0),
)

# PMK key numbers in the current horizontal orientation are arranged as:
#   3,  7, 11, 15
#   2,  6, 10, 14
#   1,  5,  9, 13
#   0,  4,  8, 12
# Map those positions to logical 0..15 so the finger-indicated top-left key is
# PC1 and commands then proceed left-to-right, top-to-bottom.
PHYSICAL_TO_LOGICAL = (
    12, 8, 4, 0,
    13, 9, 5, 1,
    14, 10, 6, 2,
    15, 11, 7, 3,
)


def validate_mapping():
    """Raise ValueError if the 16-key layout is incomplete or inconsistent."""
    if len(COMMAND_NAMES) != 16:
        raise ValueError("Command deck must define exactly 16 keys")
    if len(set(COMMAND_NAMES)) != 16:
        raise ValueError("Command names must be unique")
    if set(COMMAND_NAMES) != set(COMMAND_KEY_NAMES):
        raise ValueError("Layout names and command mappings do not match")
    if len(KEY_COLOURS) != 16:
        raise ValueError("Each key must have an RGB colour")
    if tuple(sorted(PHYSICAL_TO_LOGICAL)) != tuple(range(16)):
        raise ValueError("Physical-to-logical map must be a 0..15 permutation")
    return True
