from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    PasswordField,
    EmailField,
    BooleanField,
    SubmitField,
    TextAreaField,
    DecimalField,
    SelectField,
    FileField,
    RadioField,
)
from wtforms.validators import (
    DataRequired,
    length,
    NumberRange,
    Email,
    EqualTo,
    Length,
    Optional,
    URL,
)
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL
from flask_wtf.file import FileField, FileAllowed


class SignUpForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=50)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=50)]
    )
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password1")]
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField(
        "Enter Your Password", validators=[DataRequired(), length(min=6)]
    )
    submit = SubmitField("Log In")


class ProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    submit_profile = SubmitField("Save Changes")


class PasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_new_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Passwords must match"),
        ],
    )
    submit_password = SubmitField("Change Password")


class PropertyForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(min=10, max=500)]
    )
    current_price = DecimalField(
        "Current Price", validators=[DataRequired(), NumberRange(min=0)], places=2
    )
    location = StringField(
        "Location", validators=[DataRequired(), Length(min=5, max=100)]
    )
    category = SelectField(
        "Category",
        choices=[("Rent", "Rent"), ("Sell", "Sell")],
        validators=[DataRequired()],
    )
    image_url = FileField(
        "Image", validators=[FileAllowed(["jpg", "png"], "Images only!")]
    )
    available = BooleanField("Available")
    for_sale = BooleanField("For Sale")
    submit_property = SubmitField("Add Property")
