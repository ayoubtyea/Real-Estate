from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


# Initialize the database
db = SQLAlchemy()
DB_NAME = "database.sqlite3"


def create_database(app):
    with app.app_context():
        db.create_all()
        print("Database Created")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mY secrete Key Here"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["DEBUG"] = True

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Property, ClientProperty, Category, Request

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/")

    create_database(app)

    return app
