from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, SignUpForm, PasswordForm, ProfileForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, flash, request
from website.models import Request

auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            # Check if the email already exists
            existing_customer = Customer.query.filter_by(email=email).first()
            if existing_customer:
                flash(
                    "Email already exists. Please log in or use a different email.",
                    "danger",
                )
                return redirect(url_for("auth.sign_up"))

            new_customer = Customer(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password1,  # Password hashing is handled by the setter method
            )

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash("Successfully signed up!", "success")
                return redirect(url_for("auth.login"))
            except Exception as e:
                print(e)
                db.session.rollback()
                flash("Account could not be created due to an error.", "danger")
                # Optional: Clear form data on error
                form.email.data = ""
                form.first_name.data = ""
                form.last_name.data = ""
                form.password1.data = ""
                form.password2.data = ""
        else:
            flash("Passwords do not match", "danger")
    return render_template("signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                return redirect("/")
            else:
                flash("Incorrect Email or Password")

        else:
            flash("Account doew not exist please Sign Up")

    return render_template("login.html", form=form)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def log_out():
    logout_user()
    return redirect("/")


@auth.route("/profile/<int:customer_id>", methods=["GET", "POST"])
@login_required
def profile(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    print("Customer ID:", customer_id)

    # Ensure that the current user is the one trying to access the profile
    if customer.id != current_user.id:
        return redirect(url_for("views.home"))

    # Initialize forms
    profile_form = ProfileForm(obj=customer)
    password_form = PasswordForm()

    # Handle profile form submission
    if profile_form.submit_profile.data and profile_form.validate_on_submit():
        if (
            Customer.query.filter_by(email=profile_form.email.data).first()
            and profile_form.email.data != customer.email
        ):
            flash("Email already exists", "info_error")
        elif (
            Customer.query.filter_by(
                first_name=profile_form.first_name.data,
                last_name=profile_form.last_name.data,
            ).first()
            and profile_form.first_name.data != customer.first_name
            and profile_form.last_name.data != customer.last_name
        ):
            flash("Name already exists", "info_error")
        else:
            # Update customer details
            customer.first_name = profile_form.first_name.data
            customer.last_name = profile_form.last_name.data
            customer.email = profile_form.email.data
            customer.phone_number = profile_form.phone_number.data
            customer.address = profile_form.address.data
            db.session.commit()
            flash("Profile updated successfully", "info_success")
        return redirect(url_for("auth.profile", customer_id=customer.id))

    # Handle password form submission
    if password_form.submit_password.data and password_form.validate_on_submit():
        if customer.verify_password(password_form.current_password.data):
            customer.password = password_form.new_password.data
            db.session.commit()
            flash("Password updated successfully", "password_success")
        else:
            flash("Current password is incorrect", "password_error")
        return redirect(url_for("auth.profile", customer_id=customer.id))

    # Fetch property requests made by the customer
    requests = Request.query.filter_by(customer_id=customer.id).all()

    # Render the profile template
    return render_template(
        "profile.html",
        customer=customer,
        profile_form=profile_form,
        password_form=password_form,
        requests=requests,
    )
