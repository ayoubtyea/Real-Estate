from flask import Blueprint, render_template, current_app, jsonify, request, session
from .models import Property
from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, flash, request
from website.models import Request
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    send_from_directory,
)
from flask_login import login_required, current_user
from .models import Property
from . import db
from website.models import Request
from .models import db, Request, Property
from flask import request, render_template, redirect, url_for, flash

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    properties = Property.query.all()
    predicted_price = session.get("predicted_price")
    return render_template(
        "home.html", properties=properties, predicted_price=predicted_price
    )


@views.route("/who")
def who():
    return render_template("who_we_are.html")


@views.route("/search")
def search():
    properties = Property.query.all()
    return render_template("search.in.offers.html", properties=properties)


@views.route("/property/<int:property_id>", methods=["GET", "POST"])
def property_detail(property_id):
    property = Property.query.get_or_404(property_id)

    if request.method == "POST":
        flash("Property requested successfully!", "success")
        return redirect(url_for("property_detail", property_id=property_id))

    return render_template("property_detail.html", property=property)


# @views.route("/my_requests", methods=["GET", "POST"])
# @login_required
# def my_requests():
#     if request.method == "POST":
#         property_id = request.form.get("property_id")
#         name = request.form.get("name")
#         email = request.form.get("email")
#         message = request.form.get("message")
#         payment_id = "example-payment-id"

#         new_request = Request(
#             customer_id=current_user.id,
#             property_id=property_id,
#             message=message,
#             status="Pending",
#             payment_id=payment_id,
#         )

#         try:
#             db.session.add(new_request)
#             db.session.commit()
#             flash("Your request has been submitted successfully", "success")
#         except Exception as e:
#             db.session.rollback()
#             flash(f"An error occurred: {e}", "danger")

#         return redirect(url_for("views.my_requests"))

#     requests = Request.query.filter_by(customer_id=current_user.id).all()
#     properties = []
#     for request_item in requests:
#         property = Property.query.get(request_item.property_id)
#         if property:
#             properties.append(
#                 {
#                     "title": property.title,
#                     "id": property.id,
#                     "current_price": property.current_price,
#                     "location": property.location,
#                     "category": property.category,
#                     "image_url": property.image_url,
#                 }
#             )

#     return render_template("property_detail.html", properties=properties)


@views.route("/property/<int:property_id>/request", methods=["POST"])
@login_required
def property_request(property_id):
    property = Property.query.get_or_404(property_id)
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        payment_id = (
            "example-payment-id"  # Replace with actual payment handling if needed
        )

        new_request = Request(
            customer_id=current_user.id,
            property_id=property_id,
            message=message,
            status="Pending",
            payment_id=payment_id,
        )

        try:
            db.session.add(new_request)
            db.session.commit()
            flash("Your request has been submitted successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {e}", "danger")

        # Redirect back to the property detail page
        return redirect(url_for("views.property_detail", property_id=property_id))

    return redirect(url_for("views.property_detail", property_id=property_id))


@views.route("/profile", methods=["GET", "POST"])
@login_required
def my_requests():
    requests = Request.query.filter_by(customer_id=current_user.id).all()
    properties = []
    for request_item in requests:
        property = Property.query.get(request_item.property_id)
        if property:
            properties.append(
                {
                    "title": property.title,
                    "id": property.id,
                    "current_price": property.current_price,
                    "location": property.location,
                    "category": property.category,
                    "image_url": property.image_url,
                }
            )

    return render_template("profile.html", properties=properties)


@views.route("/predict", methods=["POST"])
def predict():
    try:
        # Get the form inputs
        bedrooms = int(request.form.get("bedrooms"))
        bathrooms = int(request.form.get("bathrooms"))
        floors = float(request.form.get("floors"))
        waterfront = int(request.form.get("waterfront"))

        # Prepare data for prediction
        input_data = [[bedrooms, bathrooms, floors, waterfront]]

        # Load the model and make prediction
        model = current_app.model
        prediction = model.predict(input_data)[0]

        # Store the predicted price in session
        session["predicted_price"] = prediction
        return redirect(url_for("views.home") + "#ai")

    except Exception as e:
        session["predicted_price"] = "Error"
        return redirect(url_for("views.home") + "#ai")
