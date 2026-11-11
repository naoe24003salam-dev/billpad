"""Discount codes.

Every code has a percentage and a last day it can be used. A code is
only applied after validate_code() has checked that it exists and
has not expired.
"""

from datetime import date

CODES = {
    "SAVE10": {"percent": 10, "expires": date(2027, 6, 30)},
    "STUDENT15": {"percent": 15, "expires": date(2026, 12, 31)},
    "OLD20": {"percent": 20, "expires": date(2026, 1, 15)},
}


class UnknownCodeError(Exception):
    """Raised when a discount code is not in the table."""


class ExpiredCodeError(Exception):
    """Raised when a discount code is past its last day."""


def validate_code(code, today=None):
    """Return the discount percent for a code, or raise.

    Raises UnknownCodeError if the code is not in the table and
    ExpiredCodeError if it is past its expiry date.
    """
    today = today or date.today()
    entry = CODES.get(code.strip().upper())
    if entry is None:
        raise UnknownCodeError("unknown discount code: %s" % code)
    if today > entry["expires"]:
        raise ExpiredCodeError(
            "discount code %s expired on %s" % (code, entry["expires"])
        )
    return entry["percent"]


def apply_discount(subtotal, code, today=None):
    """Take a validated percent off a subtotal and return the new total."""
    percent = validate_code(code, today=today)
    return subtotal - (subtotal * percent // 100)
