
"""Sprint 3: budgets, spending analytics, savings simulation, price history and sharing."""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import query, execute
from iterations.sprint1 import login_required

bp = Blueprint("sprint3", __name__)


def monthly_equivalent(amount, cycle):
    divisor = {
        "monthly": 1,
        "quarterly": 3,
        "half-yearly": 6,
        "yearly": 12
    }.get(cycle, 1)

    return float(amount) / divisor


@bp.route("/insights", methods=["GET", "POST"])
@login_required
def insights():
    rows = query(
        "SELECT * FROM subscriptions WHERE user_id=%s AND status='active'",
        (session["user_id"],)
    )

    monthly = sum(
        monthly_equivalent(r["amount"], r["billing_cycle"])
        for r in rows
    )

    budget = query(
        "SELECT * FROM budgets WHERE user_id=%s",
        (session["user_id"],),
        fetchone=True
    )

    if request.method == "POST":
        try:
            limit = float(request.form["monthly_limit"])

            if limit <= 0:
                raise ValueError()

            if budget:
                execute(
                    "UPDATE budgets SET monthly_limit=%s WHERE user_id=%s",
                    (limit, session["user_id"])
                )
            else:
                execute(
                    "INSERT INTO budgets(user_id,monthly_limit) VALUES(%s,%s)",
                    (session["user_id"], limit)
                )

            return redirect(url_for("sprint3.insights"))

        except ValueError:
            flash("Enter a positive budget amount.")

    category_totals = {}

    for r in rows:
        category_totals[r["category"]] = (
            category_totals.get(r["category"], 0)
            + monthly_equivalent(r["amount"], r["billing_cycle"])
        )

    return render_template(
        "insights.html",
        monthly=monthly,
        budget=budget,
        categories=category_totals,
        subscriptions=rows
    )


@bp.post("/subscriptions/<int:item_id>/price")
@login_required
def change_price(item_id):
    item = query(
        "SELECT * FROM subscriptions WHERE id=%s AND user_id=%s",
        (item_id, session["user_id"]),
        fetchone=True
    )

    if not item:
        flash("Subscription not found.")
        return redirect(url_for("sprint3.insights"))

    try:
        new_amount = float(request.form["new_amount"])

        if new_amount <= 0:
            raise ValueError()

        execute(
            """INSERT INTO price_history
            (subscription_id,old_amount,new_amount,changed_on)
            VALUES(%s,%s,%s,CURDATE())""",
            (item_id, item["amount"], new_amount)
        )

        execute(
            "UPDATE subscriptions SET amount=%s WHERE id=%s AND user_id=%s",
            (new_amount, item_id, session["user_id"])
        )

        flash("Price history updated.")

    except ValueError:
        flash("Enter a valid new price.")

    return redirect(url_for("sprint3.insights"))


@bp.get("/savings")
@login_required
def savings():
    rows = query(
        "SELECT * FROM subscriptions WHERE user_id=%s AND status='active'",
        (session["user_id"],)
    )

    # Simulation only: user chooses which services to consider cancelling.
    monthly_values = [
        (r, monthly_equivalent(r["amount"], r["billing_cycle"]))
        for r in rows
    ]

    return render_template("savings.html", entries=monthly_values)


@bp.route("/sharing", methods=["GET", "POST"])
@login_required
def sharing():
    if request.method == "POST":
        try:
            group_name = request.form["group_name"].strip()
            member_name = request.form["member_name"].strip()
            share = float(request.form["share_amount"])

            if not group_name or not member_name or share <= 0:
                raise ValueError()

            group = query(
                "SELECT id FROM shared_groups WHERE owner_id=%s AND group_name=%s",
                (session["user_id"], group_name),
                fetchone=True
            )

            group_id = group["id"] if group else execute(
                "INSERT INTO shared_groups(owner_id,group_name) VALUES(%s,%s)",
                (session["user_id"], group_name)
            )

            execute(
                """INSERT INTO group_members
                (group_id,member_name,share_amount)
                VALUES(%s,%s,%s)""",
                (group_id, member_name, share)
            )

            flash("Member added to shared group.")

        except (ValueError, KeyError):
            flash("Enter valid group and member details.")

        return redirect(url_for("sprint3.sharing"))

    groups = query(
        "SELECT * FROM shared_groups WHERE owner_id=%s",
        (session["user_id"],)
    )

    for g in groups:
        g["members"] = query(
            "SELECT * FROM group_members WHERE group_id=%s",
            (g["id"],)
        )

    return render_template("sharing.html", groups=groups)
