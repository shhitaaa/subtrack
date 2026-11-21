from datetime import date
from iterations.sprint2 import add_months, next_date

def test_add_months_handles_month_end():
    assert add_months(date(2026, 1, 31), 1) == date(2026, 2, 28)

def test_billing_cycle_next_date():
    assert next_date(date(2026, 1, 15), "quarterly") == date(2026, 4, 15)
    assert next_date(date(2026, 1, 15), "yearly") == date(2027, 1, 15)
