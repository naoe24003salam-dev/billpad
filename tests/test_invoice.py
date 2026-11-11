import pytest

from billpad.catalog import UnknownItemError
from billpad.invoice import Invoice


def make_invoice():
    inv = Invoice()
    inv.add("rice 5kg")       # 340
    inv.add("eggs 12", 2)     # 2 x 150
    return inv


def test_subtotal_adds_up_the_lines():
    assert make_invoice().subtotal() == 640


def test_total_without_a_code_is_the_subtotal():
    assert make_invoice().calc_total() == 640


def test_unknown_item_is_rejected():
    inv = Invoice()
    with pytest.raises(UnknownItemError):
        inv.add("caviar")
