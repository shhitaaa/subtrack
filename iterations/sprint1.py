"""Sprint 1: authentication, subscription CRUD and dashboard foundation."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import query, execute

bp = Blueprint("sprint1", __name__)

def login_required(view):
    from functools import wraps
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("sprint1.login"))
        return view(*args, **kwargs)
    return wrapped

@bp.route("/")
@login_required
def dashboard():
    rows = query("SELECT * FROM subscriptions WHERE user_id=%s AND status='active' ORDER BY next_renewal", (session["user_id"],))
    total = sum(float(r["amount"]) for r in rows if r["billing_cycle"] == "monthly")
    return render_template("dashboard.html", subscriptions=rows, monthly_total=total)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or len(password) < 8:
            flash("Enter a name, valid email and password of at least 8 characters.")
            return redirect(url_for("sprint1.register"))
        try:
            execute("INSERT INTO users(name,email,password_hash) VALUES(%s,%s,%s)",
                    (name, email, generate_password_hash(password)))
            flash("Account created. Please log in.")
            return redirect(url_for("sprint1.login"))
        except Exception:
            flash("That email may already be registered.")
    return render_template("register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = query("SELECT * FROM users WHERE email=%s", (email,), fetchone=True)
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session.clear()
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            return redirect(url_for("sprint1.dashboard"))
        flash("Incorrect email or password.")
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("sprint1.login"))

@bp.route("/subscriptions/add", methods=["GET", "POST"])
@login_required
def add_subscription():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "Other").strip()
        try:
            amount = float(request.form.get("amount", "0"))
            from datetime import date
            renewal = date.fromisoformat(request.form["next_renewal"])
            cycle = request.form.get("billing_cycle", "monthly")
            if not name or amount <= 0 or cycle not in {"monthly","quarterly","half-yearly","yearly"}:
                raise ValueError()
            execute("""INSERT INTO subscriptions(user_id,name,category,amount,billing_cycle,next_renewal)
                       VALUES(%s,%s,%s,%s,%s,%s)""",
                    (session["user_id"], name, category, amount, cycle, renewal))
            flash("Subscription added.")
            return redirect(url_for("sprint1.dashboard"))
        except (ValueError, KeyError):
            flash("Please enter valid subscription details.")
    return render_template("subscription_form.html", item=None)

@bp.route("/subscriptions/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_subscription(item_id):
    item = query("SELECT * FROM subscriptions WHERE id=%s AND user_id=%s",
                 (item_id, session["user_id"]), fetchone=True)
    if not item:
        flash("Subscription not found.")
        return redirect(url_for("sprint1.dashboard"))
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            from datetime import date
            renewal = date.fromisoformat(request.form["next_renewal"])
            execute("""UPDATE subscriptions SET name=%s,category=%s,amount=%s,billing_cycle=%s,next_renewal=%s
                       WHERE id=%s AND user_id=%s""",
                    (request.form["name"].strip(), request.form["category"].strip(), amount,
                     request.form["billing_cycle"], renewal, item_id, session["user_id"]))
            flash("Subscription updated.")
            return redirect(url_for("sprint1.dashboard"))
        except (ValueError, KeyError):
            flash("Please enter valid details.")
    return render_template("subscription_form.html", item=item)

@bp.post("/subscriptions/<int:item_id>/delete")
@login_required
def delete_subscription(item_id):
    execute("DELETE FROM subscriptions WHERE id=%s AND user_id=%s", (item_id, session["user_id"]))
    flash("Subscription deleted.")
    return redirect(url_for("sprint1.dashboard"))
