import os
import pickle
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize the database and migrate
db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.sqlite3"


def create_database(app):
    with app.app_context():
        db.create_all()
        print("Database Created")


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URI", f"sqlite:///{DB_NAME}"
    )
    app.config["DEBUG"] = True

    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Define the user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))

    # Register blueprints
    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer, Property, ClientProperty, Category, Request

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/")

    # Load the model
    model_path = os.path.join(app.root_path, "static", "models", "model.pkl")
    if os.path.isfile(model_path):
        try:
            with open(model_path, "rb") as file:
                app.model = pickle.load(file)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Failed to load model: {e}")
    else:
        print(f"Model file not found at {model_path}")

    # Create the database if it doesn't exist
    create_database(app)

    # Error handling
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app
