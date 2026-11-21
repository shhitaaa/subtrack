from datetime import date
from iterations.sprint2 import add_months, next_date


# Test add_months()

def test_add_months_handles_month_end():
    assert add_months(date(2026, 1, 31), 1) == date(2026, 2, 28)


def test_add_months_handles_leap_year():
    assert add_months(date(2028, 1, 31), 1) == date(2028, 2, 29)


def test_add_months_crosses_year():
    assert add_months(date(2026, 12, 15), 1) == date(2027, 1, 15)


def test_add_multiple_months():
    assert add_months(date(2026, 1, 31), 2) == date(2026, 3, 31)


# Test next_date()

def test_monthly_billing_cycle():
    assert next_date(date(2026, 1, 15), "monthly") == date(2026, 2, 15)


def test_quarterly_billing_cycle():
    assert next_date(date(2026, 1, 15), "quarterly") == date(2026, 4, 15)


def test_half_yearly_billing_cycle():
    assert next_date(date(2026, 1, 15), "half-yearly") == date(2026, 7, 15)


def test_yearly_billing_cycle():
    assert next_date(date(2026, 1, 15), "yearly") == date(2027, 1, 15)


def test_invalid_billing_cycle():
    assert next_date(date(2026, 1, 15), "invalid") == date(2026, 1, 15)