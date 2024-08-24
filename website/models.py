from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f"<Customer {self.id}>"


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    available = db.Column(db.Boolean, default=True)
    for_sale = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Ensure unique backref name
    requests = db.relationship("Request", back_populates="property")

    def __str__(self):
        return f"<Property {self.title}>"


class ClientProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    interest_type = db.Column(db.String(50), nullable=False)
    customer = db.relationship(
        "Customer", backref=db.backref("client_properties", lazy=True)
    )
    property = db.relationship(
        "Property", backref=db.backref("client_properties", lazy=True)
    )

    def __str__(self):
        return f"<ClientProperty {self.customer_id} - {self.property_id}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __str__(self):
        return f"<Category {self.name}>"


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="Pending")
    payment_id = db.Column(db.String(1000), nullable=True)

    # Relationships
    customer = db.relationship("Customer", backref=db.backref("requests", lazy=True))
    property = db.relationship("Property", back_populates="requests")

    def __str__(self):
        return f"<Request {self.customer_id} - {self.property_id}>"
