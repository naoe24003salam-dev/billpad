"""The price list. Prices are in taka, per piece or per kg as sold."""

PRICES = {
    "rice 5kg": 340,
    "rice 1kg": 72,
    "lentils 1kg": 145,
    "cooking oil 1l": 190,
    "cooking oil 5l": 920,
    "sugar 1kg": 120,
    "salt 1kg": 42,
    "tea 200g": 165,
    "biscuits": 60,
    "soap": 55,
    "detergent 500g": 130,
    "eggs 12": 150,
    "milk 1l": 95,
    "flour 2kg": 150,
    "onion 1kg": 68,
    "potato 1kg": 45,
}


class UnknownItemError(Exception):
    """Raised when an item is not on the price list."""


def price_of(item):
    try:
        return PRICES[item]
    except KeyError:
        raise UnknownItemError("no price for item: %s" % item)
