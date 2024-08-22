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
from datetime import datetime
from .forms import PropertyForm
from werkzeug.utils import secure_filename
from .forms import PropertyForm
from flask import current_app
import os
from website.models import Request


admin = Blueprint("admin", __name__)


@admin.route("/media/<path:filename>")
def get_image(filename):
    return send_from_directory("../media", filename)


@admin.route("/manage-properties", methods=["GET", "POST"])
@login_required
def manage_properties():
    if current_user.id == 1:
        form = PropertyForm()
        edit_form = None
        edit_property = None
        edit_property_id = request.args.get("edit")

    # Handle adding a new property
    if form.validate_on_submit() and not edit_property_id:
        image_filename = None
        if form.image_url.data:
            image_file = form.image_url.data
            image_filename = secure_filename(image_file.filename)
            media_dir = os.path.join(current_app.root_path, "..", "media")
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
        try:
            db.session.add(new_property)
            db.session.commit()
            flash("Property added successfully", "success")
            return redirect(url_for("admin.manage_properties"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding property: {e}", "danger")

    # Handle editing an existing property
    if edit_property_id:
        edit_property = Property.query.get_or_404(edit_property_id)
        edit_form = PropertyForm(obj=edit_property)
        if edit_form.validate_on_submit():
            edit_property.title = edit_form.title.data
            edit_property.description = edit_form.description.data
            edit_property.current_price = edit_form.current_price.data
            edit_property.location = edit_form.location.data
            edit_property.category = edit_form.category.data

            if edit_form.image_url.data:
                if (
                    hasattr(edit_form.image_url.data, "filename")
                    and edit_form.image_url.data.filename
                ):
                    image_file = edit_form.image_url.data
                    if image_file.read(1):  # Check if file has content
                        image_filename = secure_filename(image_file.filename)
                        media_dir = os.path.join(current_app.root_path, "..", "media")
                        image_file.save(os.path.join(media_dir, image_filename))
                        edit_property.image_url = image_filename
                    edit_form.image_url.data.seek(0)  # Reset file pointer

            edit_property.available = edit_form.available.data
            edit_property.for_sale = edit_form.for_sale.data

            db.session.commit()
            flash("Property updated successfully", "success")
            return redirect(url_for("admin.manage_properties"))

    # Query to filter properties based on `category` and `for_sale`
    category_filter = request.args.get("category", "all")
    properties = Property.query.filter(
        (Property.category == category_filter) | (category_filter == "all")
    ).all()

    requests = Request.query.all()
    # Handle Approve/Reject actions for customer property requests
    if request.method == "POST":
        request_id = request.form.get("request_id")
        action = request.form.get("action")
        req = Request.query.get_or_404(request_id)

        if action == "approve":
            req.status = "Approved"
            flash("Request Approved", "success")
        elif action == "reject":
            req.status = "Rejected"
            flash("Request Rejected", "danger")

        db.session.commit()
        return redirect(url_for("admin.manage_properties"))

    return render_template(
        "manage_properties.html",
        form=form,
        edit_form=edit_form,
        edit_property=edit_property,
        properties=properties,
        requests=requests,
    )


@admin.route("/delete-property/<int:property_id>", methods=["POST"])
@login_required
def delete_property(property_id):
    if current_user.id == 1:

        property = Property.query.get_or_404(property_id)
        db.session.delete(property)
        db.session.commit()
        flash("Property deleted successfully", "success")
        return redirect(url_for("admin.manage_properties"))


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
