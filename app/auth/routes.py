from flask import flash, redirect, render_template, request, url_for
from flask_babel import _
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.auth import auth_bp
from app.auth.email import send_password_reset_email
from app.auth.forms import (LoginForm, RegistrationForm, ResetPasswordForm,
                            ResetPasswordRequestForm)
from app.models import User


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_("Invalid username or password"))
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)

        next = request.args.get("next")
        if not next or url_parse(next).netloc != "":
            next = url_for("core.index")

        return redirect(next)

    return render_template("auth/login.html", title=_("Sign In"), form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(_("Congratulations, you are now a registered user!"))

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", title=_("Register"), form=form)


@auth_bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            send_password_reset_email()

        flash(_("Check your email for the instructions to reset your password"))
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/reset_password_request.html", title=_("Reset Password"), form=form
    )


@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token: str):
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("core.index"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)

        db.session.commit()

        flash(_("Your password has been reset."))
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", form=form)
