
"""Sprint 2: recurring billing, renewal calculations and reminder list."""

from datetime import date, timedelta
from calendar import monthrange
from flask import Blueprint, render_template, session, request
from db import query
from iterations.sprint1 import login_required

bp = Blueprint("sprint2", __name__)


def add_months(day, months):
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    return date(year, month, min(day.day, monthrange(year, month)[1]))


def next_date(current, cycle):
    months = {
        "monthly": 1,
        "quarterly": 3,
        "half-yearly": 6,
        "yearly": 12
    }.get(cycle)

    return add_months(current, months) if months else current


@bp.get("/renewals")
@login_required
def renewals():
    today = date.today()
    upcoming_limit = today + timedelta(days=30)

    cycle = request.args.get("cycle", "")
    sort = request.args.get("sort", "nearest")

    # Existing renewal list
    sql = """SELECT * FROM subscriptions
             WHERE user_id=%s
             AND status='active'
             AND next_renewal <= %s"""

    params = [session["user_id"], upcoming_limit]

    if cycle in ("monthly", "quarterly", "half-yearly", "yearly"):
        sql += " AND billing_cycle=%s"
        params.append(cycle)

    if sort == "latest":
        sql += " ORDER BY next_renewal DESC"
    else:
        sql += " ORDER BY next_renewal ASC"

    rows = query(sql, tuple(params))

    # Calendar data: all active subscriptions
    calendar_rows = query(
        """SELECT name, next_renewal
           FROM subscriptions
           WHERE user_id=%s AND status='active'""",
        (session["user_id"],)
    )

    calendar_events = [
        {
            "date": s["next_renewal"].isoformat(),
            "name": s["name"]
        }
        for s in calendar_rows
        if s["next_renewal"] is not None
    ]

    return render_template(
        "renewals.html",
        subscriptions=rows,
        today=today,
        selected_cycle=cycle,
        selected_sort=sort,
        calendar_events=calendar_events
    )
