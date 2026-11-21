"""Sprint 2: recurring billing, renewal calculations and reminder list."""
from datetime import date, timedelta
from calendar import monthrange
from flask import Blueprint, render_template, session
from db import query
from iterations.sprint1 import login_required

bp = Blueprint("sprint2", __name__)

def add_months(day, months):
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    return date(year, month, min(day.day, monthrange(year, month)[1]))

def next_date(current, cycle):
    months = {"monthly": 1, "quarterly": 3, "half-yearly": 6, "yearly": 12}.get(cycle)
    return add_months(current, months) if months else current

@bp.get("/renewals")
@login_required
def renewals():
    rows = query("""SELECT * FROM subscriptions
                    WHERE user_id=%s AND status='active' AND next_renewal <= %s
                    ORDER BY next_renewal""",
                 (session["user_id"], date.today() + timedelta(days=30)))
    return render_template("renewals.html", subscriptions=rows, today=date.today())
