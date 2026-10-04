"""Host-side checks for the Pico command-deck mapping."""

import pathlib
import sys

PROJECT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
sys.path.insert(0, str(PROJECT / "lib"))

from adafruit_hid.keycode import Keycode
from tesmart_commands import (
    COMMAND_KEY_NAMES,
    COMMAND_NAMES,
    KEY_COLOURS,
    PHYSICAL_TO_LOGICAL,
    PREFIX_NAMES,
    validate_mapping,
)


def main():
    assert validate_mapping() is True
    assert len(COMMAND_NAMES) == 16
    assert COMMAND_NAMES[:4] == ("PC1", "PC2", "MON1", "MON2")
    assert COMMAND_NAMES[-4:] == (
        "LIGHTS_OFF",
        "LIGHTS_LINKED",
        "LIGHTS_MARQUEE",
        "LIGHTS_BREATHE",
    )
    assert PREFIX_NAMES == ("GRAVE_ACCENT", "GRAVE_ACCENT")
    assert COMMAND_KEY_NAMES["FOCUS"] == ("RIGHT_ALT", "RIGHT_ALT")
    assert COMMAND_KEY_NAMES["LIGHTS_BREATHE"] == ("L", "THREE")
    assert len(KEY_COLOURS) == 16
    assert KEY_COLOURS[0] == KEY_COLOURS[1] == (0, 90, 255)
    assert KEY_COLOURS[2] == KEY_COLOURS[3] == KEY_COLOURS[4] == (255, 25, 20)
    assert KEY_COLOURS[-4:] == (
        (30, 30, 30),
        (160, 0, 255),
        (255, 0, 120),
        (255, 70, 0),
    )

    # PMK numbers run bottom-to-top by columns in the current orientation.
    # This permutation makes the finger-indicated top-left key logical PC1.
    assert PHYSICAL_TO_LOGICAL == (
        12, 8, 4, 0,
        13, 9, 5, 1,
        14, 10, 6, 2,
        15, 11, 7, 3,
    )

    for key_name in PREFIX_NAMES:
        assert hasattr(Keycode, key_name), key_name
    for sequence in COMMAND_KEY_NAMES.values():
        for key_name in sequence:
            assert hasattr(Keycode, key_name), key_name

    print("mapping test: PASS")
    print("16 commands:", ", ".join(COMMAND_NAMES))


if __name__ == "__main__":
    main()
