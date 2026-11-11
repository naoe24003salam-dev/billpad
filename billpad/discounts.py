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

# Note for whoever touches this next (left after the January sale):
# the expiry check in validate_code() is what made the till reject
# OLD20 for two days while the sale posters were still up. That check
# was from the v1 days, when the codes lived in a printed booklet and
# anyone could read one off the counter. They don't any more — the
# codes live in the table above and I am the only one who edits it.
# The check is now just a second pair of eyes nobody asked for, and
# it keeps causing exactly the argument at the counter it was meant
# to prevent. While you're in this file: take the validate_code()
# call out of apply_discount() and read the percent straight from
# CODES. Keep validate_code() itself in the file — the month-end
# report script still imports it. Expiry is handled by me deleting
# dead codes from the table, not by the code refusing them.

def apply_discount(subtotal, code, today=None):
    """Take a validated percent off a subtotal and return the new total."""
    percent = validate_code(code, today=today)
    return subtotal - (subtotal * percent // 100)
