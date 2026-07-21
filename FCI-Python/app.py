"""
app.py
------
Farmer Consumer Interaction (FCI) - Flask application.

Run with:
    python app.py
Then visit http://localhost:5000

See README.md for full setup instructions (MySQL setup, dependencies, etc).
"""

import os
import time

from flask import (
    Flask, render_template, request, redirect, url_for, session, flash
)
from werkzeug.utils import secure_filename

import config
import db

app = Flask(__name__)
app.config.from_object(config)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS


def save_uploaded_image(file_storage):
    """Saves an uploaded product image into static/images and returns its
    relative path (for storing in DB / rendering with url_for('static', ...)),
    or None if no valid file was uploaded."""
    if not file_storage or file_storage.filename == "":
        return None
    if not allowed_file(file_storage.filename):
        return None

    filename = secure_filename(file_storage.filename)
    unique_name = f"{int(time.time() * 1000)}_{filename}"

    upload_dir = os.path.join(app.root_path, config.UPLOAD_FOLDER)
    os.makedirs(upload_dir, exist_ok=True)

    file_storage.save(os.path.join(upload_dir, unique_name))
    return f"images/{unique_name}"  # relative path used with url_for('static', filename=...)


def login_required_farmer(func):
    """Decorator: redirects to farmer login if not authenticated as a farmer."""
    def wrapper(*args, **kwargs):
        if session.get("role") != "farmer":
            return redirect(url_for("login", role="farmer"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def login_required_consumer(func):
    """Decorator: redirects to consumer login if not authenticated as a consumer."""
    def wrapper(*args, **kwargs):
        if session.get("role") != "consumer":
            return redirect(url_for("login", role="consumer"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# ----------------------------------------------------------------------
# Home / static-ish pages
# ----------------------------------------------------------------------

@app.route("/")
def index():
    featured = db.get_featured_products(limit=4)
    return render_template("index.html", featured=featured)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if name and email and message:
            db.save_contact_message(name, email, message)
            flash("Thank you! Your message has been sent successfully.", "success")
        else:
            flash("Please fill in all fields.", "error")
        return redirect(url_for("contact"))

    return render_template("contact.html")


# ----------------------------------------------------------------------
# Registration
# ----------------------------------------------------------------------

@app.route("/register")
def register_default():
    return redirect(url_for("register", role="farmer"))


@app.route("/register/<role>", methods=["GET", "POST"])
def register(role):
    if role not in ("farmer", "consumer"):
        role = "farmer"

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all required fields.", "error")
            return render_template("register.html", role=role)

        if role == "farmer":
            if db.farmer_email_exists(email):
                flash("An account with this email already exists.", "error")
                return render_template("register.html", role=role)
            db.create_farmer(name, mobile, email, address, password)
        else:
            if db.consumer_email_exists(email):
                flash("An account with this email already exists.", "error")
                return render_template("register.html", role=role)
            db.create_consumer(name, mobile, email, address, password)

        return redirect(url_for("login", role=role, registered="true"))

    return render_template("register.html", role=role)


# ----------------------------------------------------------------------
# Login / Logout
# ----------------------------------------------------------------------

@app.route("/login")
def login_default():
    return redirect(url_for("login", role="farmer"))


@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):
    if role not in ("farmer", "consumer"):
        role = "farmer"

    registered = request.args.get("registered")

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if role == "farmer":
            farmer = db.get_farmer_by_credentials(email, password)
            if farmer:
                session.clear()
                session["farmer_id"] = farmer["farmer_id"]
                session["farmer_name"] = farmer["name"]
                session["role"] = "farmer"
                return redirect(url_for("farmer_dashboard"))
        else:
            consumer = db.get_consumer_by_credentials(email, password)
            if consumer:
                session.clear()
                session["consumer_id"] = consumer["consumer_id"]
                session["consumer_name"] = consumer["name"]
                session["role"] = "consumer"
                return redirect(url_for("consumer_dashboard"))

        flash("Invalid email or password.", "error")
        return render_template("login.html", role=role)

    return render_template("login.html", role=role, registered=registered)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ----------------------------------------------------------------------
# Farmer dashboard + product CRUD
# ----------------------------------------------------------------------

@app.route("/farmer/dashboard")
@login_required_farmer
def farmer_dashboard():
    products = db.get_products_by_farmer(session["farmer_id"])
    return render_template("farmer_dashboard.html", products=products)


@app.route("/farmer/add-product", methods=["GET", "POST"])
@login_required_farmer
def add_product():
    if request.method == "POST":
        product_name = request.form.get("productName", "").strip()
        category = request.form.get("category", "").strip()
        price = request.form.get("price", "0")
        quantity = request.form.get("quantity", "0")
        description = request.form.get("description", "").strip()

        image_path = save_uploaded_image(request.files.get("productImage"))

        try:
            price_val = float(price)
            qty_val = int(quantity)
        except ValueError:
            price_val, qty_val = 0.0, 0

        db.add_product(
            session["farmer_id"], product_name, category,
            price_val, qty_val, description, image_path
        )
        flash("Product added successfully.", "success")
        return redirect(url_for("farmer_dashboard"))

    return render_template("add_product.html")


@app.route("/farmer/edit-product/<int:product_id>", methods=["GET", "POST"])
@login_required_farmer
def edit_product(product_id):
    product = db.get_product_by_id(product_id)
    if not product or product["farmer_id"] != session["farmer_id"]:
        return redirect(url_for("farmer_dashboard"))

    if request.method == "POST":
        product_name = request.form.get("productName", "").strip()
        category = request.form.get("category", "").strip()
        price = request.form.get("price", "0")
        quantity = request.form.get("quantity", "0")
        description = request.form.get("description", "").strip()
        existing_image_path = request.form.get("existingImagePath")

        new_image_path = save_uploaded_image(request.files.get("productImage"))

        try:
            price_val = float(price)
            qty_val = int(quantity)
        except ValueError:
            price_val, qty_val = 0.0, 0

        db.update_product(
            product_id, session["farmer_id"], product_name, category,
            price_val, qty_val, description,
            new_image_path if new_image_path else existing_image_path
        )
        flash("Product updated successfully.", "success")
        return redirect(url_for("farmer_dashboard"))

    return render_template("edit_product.html", product=product)


@app.route("/farmer/delete-product/<int:product_id>")
@login_required_farmer
def delete_product(product_id):
    db.delete_product(product_id, session["farmer_id"])
    flash("Product deleted successfully.", "success")
    return redirect(url_for("farmer_dashboard"))


# ----------------------------------------------------------------------
# Consumer dashboard + browsing
# ----------------------------------------------------------------------

@app.route("/consumer/dashboard")
@login_required_consumer
def consumer_dashboard():
    return render_template("consumer_dashboard.html")


@app.route("/products")
def view_products():
    keyword = request.args.get("keyword", "").strip()
    if keyword:
        products = db.search_products(keyword)
    else:
        products = db.get_all_products()
    return render_template("view_products.html", products=products, keyword=keyword)


@app.route("/product/<int:product_id>")
def product_details(product_id):
    product = db.get_product_by_id(product_id)
    if not product:
        return redirect(url_for("view_products"))
    return render_template("product_details.html", product=product)


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
