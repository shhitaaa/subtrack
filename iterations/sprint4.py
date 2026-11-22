"""Sprint 4: overlap detection, notifications and shared-cost settlement."""
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from db import query, execute
from iterations.sprint1 import login_required

bp = Blueprint("sprint4", __name__)

# Category overlap is a heuristic: it flags categories with multiple active subscriptions.
@bp.get("/overlaps")
@login_required
def overlaps():
    rows = query("""SELECT category, COUNT(*) AS total, GROUP_CONCAT(name SEPARATOR ', ') AS names
                    FROM subscriptions WHERE user_id=%s AND status='active'
                    GROUP BY category HAVING COUNT(*) > 1""", (session["user_id"],))
    return render_template("overlaps.html", overlaps=rows)

@bp.get("/notifications")
@login_required
def notifications():
    rows = query("SELECT * FROM notifications WHERE user_id=%s ORDER BY created_at DESC",
                 (session["user_id"],))
    return render_template("notifications.html", notifications=rows)

@bp.post("/notifications/generate")
@login_required
def generate_notifications():
    rows = query("""SELECT name,next_renewal FROM subscriptions
                    WHERE user_id=%s AND status='active' AND next_renewal BETWEEN CURDATE()
                    AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)""", (session["user_id"],))
    for row in rows:
        execute("INSERT INTO notifications(user_id,message) VALUES(%s,%s)",
                (session["user_id"], f'{row["name"]} renews on {row["next_renewal"]}.'))
    flash(f"Created {len(rows)} renewal reminder(s).")
    return redirect(url_for("sprint4.notifications"))

@bp.post("/sharing/member/<int:member_id>/payment")
@login_required
def record_payment(member_id):
    member = query("""SELECT gm.*, sg.owner_id FROM group_members gm
                      JOIN shared_groups sg ON sg.id=gm.group_id
                      WHERE gm.id=%s AND sg.owner_id=%s""", (member_id, session["user_id"]), fetchone=True)
    if not member:
        flash("Shared member not found.")
        return redirect(url_for("sprint3.sharing"))
    try:
        paid = float(request.form["paid_amount"])
        if paid <= 0 or paid + float(member["paid_amount"]) > float(member["share_amount"]):
            raise ValueError()
        execute("UPDATE group_members SET paid_amount=paid_amount+%s WHERE id=%s", (paid, member_id))
        flash("Payment contribution recorded.")
    except ValueError:
        flash("Enter a valid amount not exceeding the outstanding balance.")
    return redirect(url_for("sprint3.sharing"))
