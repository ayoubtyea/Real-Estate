# Real Estate Flask App

A web application for renting and selling properties built using Flask, HTML, Tailwind CSS, and JavaScript. The app includes features such as user authentication, property management, and property requests, with role-based access for customers and admins.

## Features

- Browse properties for sale and rent.
- User authentication with roles (Admin and Customer).
- Property request functionality for customers.
- Admin panel for managing properties (add, edit, delete).
- Image upload functionality for properties.
- Responsive design using Tailwind CSS.
- Property price prediction using a machine learning model.
- Database-backed app using SQLAlchemy ORM.
  
## Technologies Used

- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database management
- **Jinja2** - Templating engine for dynamic HTML rendering
- **HTML5/CSS3** - Structure and styling for web pages
- **Tailwind CSS** - Utility-first CSS framework for responsive design
- **JavaScript** - Enhancing interactivity on the frontend
- **SQLite** or **PostgreSQL** - Database for storing app data
- **Machine Learning** - Pre-trained model for property pricing (scikit-learn)

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ayoubtyea/Real-Estate-app.git
    cd Real-Estate-app
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    Initialize the database and apply migrations:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. **Run the application**:
    Start the Flask development server:
    ```bash
    flask run
    ```
    The app will be running at `http://localhost:5000/`.

## Usage

- After starting the server, visit `http://localhost:5000/` to access the app.
- You can register a new customer account or log in as an admin with the default credentials:
  - **Admin Login**: `admin@example.com / password`
  
### Admin Capabilities

- View, add, update, and delete properties.
- View customer property requests.

### Customer Capabilities

- Browse available properties.
- Request to rent or purchase properties.
- View your own property requests in your profile.

## File Structure

