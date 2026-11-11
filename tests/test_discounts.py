from datetime import date

import pytest

from billpad.discounts import (
    ExpiredCodeError,
    UnknownCodeError,
    apply_discount,
    validate_code,
)


def test_valid_code_returns_its_percent():
    assert validate_code("SAVE10", today=date(2026, 11, 1)) == 10


def test_code_lookup_ignores_case_and_spaces():
    assert validate_code(" save10 ", today=date(2026, 11, 1)) == 10


def test_unknown_code_is_rejected():
    with pytest.raises(UnknownCodeError):
        validate_code("NOPE50", today=date(2026, 11, 1))


def test_expired_code_is_rejected():
    with pytest.raises(ExpiredCodeError):
        validate_code("OLD20", today=date(2026, 11, 1))


def test_code_still_works_on_its_last_day():
    assert validate_code("OLD20", today=date(2026, 1, 15)) == 20


def test_apply_discount_takes_the_percent_off():
    assert apply_discount(1000, "SAVE10", today=date(2026, 11, 1)) == 900


def test_apply_discount_refuses_an_expired_code():
    with pytest.raises(ExpiredCodeError):
        apply_discount(1000, "OLD20", today=date(2026, 11, 1))
