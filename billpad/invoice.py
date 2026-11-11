"""Building one bill: lines, a subtotal, an optional discount code."""

from .catalog import price_of
from .discounts import apply_discount


class Invoice:
    def __init__(self):
        self.lines = []  # (item, qty, unit_price)
        self.code = None

    def add(self, item, qty=1):
        price = price_of(item)
        self.lines.append((item, qty, price))

    def use_code(self, code):
        self.code = code

    def subtotal(self):
        return sum(qty * price for _item, qty, price in self.lines)

    def calc_total(self):
        total = self.subtotal()
        if self.code:
            total = apply_discount(total, self.code)
        return total

    def render(self):
        out = []
        for item, qty, price in self.lines:
            out.append("%-18s x%-3d %6d" % (item, qty, qty * price))
        out.append("-" * 30)
        out.append("%-22s %6d" % ("Subtotal", self.subtotal()))
        if self.code:
            out.append("%-22s %s" % ("Discount code", self.code))
        out.append("%-22s %6d" % ("Total", self.calc_total()))
        return "\n".join(out)
