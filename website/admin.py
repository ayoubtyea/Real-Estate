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
from .models import Property, Customer
from . import db
from datetime import datetime
from .forms import PropertyForm
from werkzeug.utils import secure_filename
from .forms import PropertyForm
from flask import current_app
import os
from website.models import Request
from flask import abort

admin = Blueprint("admin", __name__)


@admin.route("/media/<path:filename>")
def get_image(filename):
    return send_from_directory("../media", filename)


@admin.route("/manage-properties", methods=["GET", "POST"])
@login_required
def manage_properties():
    if current_user.id == 1:  # Ensure only admin can access
        form = PropertyForm()
        edit_form = None
        edit_property = None
        edit_property_id = request.args.get("edit")

        # Handle adding a new property
        if form.validate_on_submit() and not edit_property_id:
            try:
                image_filename = None
                if form.image_url.data:
                    image_file = form.image_url.data
                    image_filename = secure_filename(image_file.filename)
                    media_dir = os.path.join(current_app.root_path, "..", "media")
                    if not os.path.exists(media_dir):
                        os.makedirs(media_dir)
                    image_file.save(os.path.join(media_dir, image_filename))

                new_property = Property(
                    title=form.title.data,
                    description=form.description.data,
                    current_price=form.current_price.data,
                    location=form.location.data,
                    category=form.category.data,
                    image_url=image_filename,
                    available=form.available.data,
                    for_sale=form.for_sale.data,
                    date_added=datetime.utcnow(),
                )
                db.session.add(new_property)
                db.session.commit()
                flash("Property added successfully", "success")
                return redirect(url_for("admin.manage_properties"))
            except Exception as e:
                db.session.rollback()
                flash(f"Error adding property: {e}", "danger")
                print(f"Error adding property: {e}")

        # Handle editing an existing property
        if edit_property_id:
            edit_property = Property.query.get_or_404(edit_property_id)
            edit_form = PropertyForm(obj=edit_property)
            if edit_form.validate_on_submit():
                try:
                    edit_property.title = edit_form.title.data
                    edit_property.description = edit_form.description.data
                    edit_property.current_price = edit_form.current_price.data
                    edit_property.location = edit_form.location.data
                    edit_property.category = edit_form.category.data
                    edit_property.available = edit_form.available.data
                    edit_property.for_sale = edit_form.for_sale.data

                    if edit_form.image_url.data:
                        if (
                            hasattr(edit_form.image_url.data, "filename")
                            and edit_form.image_url.data.filename
                        ):
                            image_file = edit_form.image_url.data
                            if image_file.read(1):  # Check if file has content
                                image_filename = secure_filename(image_file.filename)
                                media_dir = os.path.join(
                                    current_app.root_path, "..", "media"
                                )
                                if not os.path.exists(media_dir):
                                    os.makedirs(media_dir)
                                image_file.save(os.path.join(media_dir, image_filename))
                                edit_property.image_url = image_filename
                            edit_form.image_url.data.seek(0)  # Reset file pointer

                    db.session.commit()
                    flash("Property updated successfully", "success")
                    return redirect(url_for("admin.manage_properties"))
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error updating property: {e}", "danger")
                    print(f"Error updating property: {e}")

        # Query to filter properties based on `category` and `for_sale`
        category_filter = request.args.get("category", "all")
        properties = Property.query.filter(
            (Property.category == category_filter) | (category_filter == "all")
        ).all()

        # Handle Approve/Reject actions for customer property requests
        if request.method == "POST":
            request_id = request.form.get("request_id")
            action = request.form.get("action")
            if request_id and action:
                req = Request.query.get_or_404(request_id)
                try:
                    if action == "approve":
                        req.status = "Approved"
                        flash("Request Approved", "success")
                    elif action == "reject":
                        req.status = "Rejected"
                        flash("Request Rejected", "danger")

                    db.session.commit()
                    return redirect(url_for("admin.manage_properties"))
                except Exception as e:
                    db.session.rollback()
                    flash(f"Error handling request: {e}", "danger")
                    print(f"Error handling request: {e}")

        # Fetch requests and customers for display
        requests = Request.query.all()
        customers = Customer.query.all()
        admin = Customer.query.get_or_404(current_user.id)

        return render_template(
            "manage_properties.html",
            form=form,
            edit_form=edit_form,
            edit_property=edit_property,
            properties=properties,
            requests=requests,
            customers=customers,
            admin=admin,
        )
    else:
        abort(404)


@admin.route("/delete-property/<int:property_id>", methods=["POST"])
@login_required
def delete_property(property_id):
    if current_user.id == 1:
        try:
            property = Property.query.get_or_404(property_id)

            # Delete or handle requests related to the property
            related_requests = Request.query.filter_by(property_id=property_id).all()

            # Option 1: Delete all related requests
            for req in related_requests:
                db.session.delete(req)

            # Option 2: Alternatively, if you want to keep the requests but set property_id to NULL,
            # uncomment the lines below and make sure the `property_id` in the Request model can be nullable.
            # for req in related_requests:
            #     req.property_id = None

            # Delete the property after handling related requests
            db.session.delete(property)
            db.session.commit()

            flash("Property and related requests deleted successfully", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting property: {e}", "danger")
            print(f"Error deleting property: {e}")

        return redirect(url_for("admin.manage_properties"))
    else:
        abort(404)


# @admin.route("/manage_requests")
# @login_required
# def manage_requests():
#     if current_user.id == 1:  # Assuming admin has an ID of 1
#         requests = Request.query.all()
#         return render_template("manage_requests.html", requests=requests)


@admin.route("/manage-requests", methods=["POST"])
@login_required
def manage_requests():
    if not current_user.is_admin:
        return redirect(url_for("home"))

    request_id = request.form.get("request_id")
    action = request.form.get("action")

    # Fetch the request from the database
    req = Request.query.get_or_404(request_id)

    # Handle actions
    if action == "approve":
        req.status = "Approved"
        db.session.commit()
        flash("Request approved successfully", "success")
    elif action == "delete":
        db.session.delete(req)
        db.session.commit()
        flash("Request deleted successfully", "danger")

    return redirect(url_for("admin.manage_requests"))


@admin.route("/view-customers")
@login_required
def view_customers():
    # Ensure only admin (id == 1) can access
    if current_user.id != 1:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("main.index"))

    customers = Customer.query.all()  # Fetch all customers

    return redirect(url_for("admin.manage_properties"), customers=customers)
