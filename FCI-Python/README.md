# Farmer Consumer Interaction (FCI) — Python / Flask Version

A simple, responsive web application that lets **farmers sell their produce
directly to consumers**, without middlemen. This is the **Python (Flask)**
version of the project — same features as the Java/JSP version, rebuilt with
Flask, Jinja2 templates, and PyMySQL.

---

## 1. Technology Stack

| Layer      | Technology                          |
|------------|---------------------------------------|
| Frontend   | HTML5, CSS3, JavaScript, Jinja2 templates |
| Backend    | Python 3, Flask                       |
| Database   | MySQL (via PyMySQL)                   |
| Server     | Flask's built-in dev server (or Gunicorn for production) |

---

## 2. Folder Structure

```
FCI-Python/
│
├── app.py                    Flask app: all routes/controllers
├── db.py                     All SQL queries (the "DAO" layer)
├── config.py                 DB credentials & app settings
├── requirements.txt          Python dependencies
│
├── templates/                Jinja2 HTML templates
│   ├── base.html             Shared navbar/footer layout
│   ├── index.html            Home page
│   ├── register.html         Registration (farmer/consumer)
│   ├── login.html            Login (farmer/consumer)
│   ├── farmer_dashboard.html
│   ├── add_product.html
│   ├── edit_product.html
│   ├── consumer_dashboard.html
│   ├── view_products.html
│   ├── product_details.html
│   └── contact.html
│
├── static/
│   ├── css/style.css         Green & white responsive theme
│   ├── js/script.js          Nav toggle, image preview, validation
│   └── images/                Uploaded product images are saved here
│
├── database/
│   └── farmer_consumer.sql   Full schema + sample data
│
└── README.md
```

---

## 3. Prerequisites

1. **Python 3.9+** installed (`python3 --version`)
2. **MySQL Server 5.7+ / 8.x** installed and running
3. `pip` for installing dependencies

---

## 4. Setup Instructions

### Step 1 — Create the database

```bash
mysql -u root -p < database/farmer_consumer.sql
```

This creates the `farmer_consumer` database with four tables
(`farmers`, `consumers`, `products`, `contact_messages`) and a couple of
sample rows so you have something to see immediately.

### Step 2 — Create a virtual environment & install dependencies

```bash
cd FCI-Python
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3 — Configure the DB connection

Open `config.py` and update the credentials to match your local MySQL setup
(or set them as environment variables — both work):

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"     # <-- change this
DB_NAME = "farmer_consumer"
```

Or, without editing the file:

```bash
export FCI_DB_USER=root
export FCI_DB_PASSWORD=your_password
export FCI_DB_NAME=farmer_consumer
```

### Step 4 — Run the app

```bash
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## 5. Try It Out

1. Register a new **Farmer** account, log in, and try **Add Product**
   (including an image upload — it's saved under `static/images/`).
2. Register a new **Consumer** account, log in, browse/search products,
   then open a product's details page to see the farmer's contact number.
3. Try the **Contact Us** form — messages are stored in the
   `contact_messages` table.

You can also log in with the sample farmer account seeded by the SQL script:
- Email: `ramesh@example.com`
- Password: `ramesh123`

---

## 6. Key Features Implemented

- Separate registration & login for **Farmers** and **Consumers**
- Session-based authentication (Flask `session`), with `@login_required_*`
  decorators guarding protected routes
- Farmer Dashboard: Add / Edit / Delete / View own products (full CRUD)
- Consumer Dashboard: View all products, keyword search (by name/category),
  view product details, and see the farmer's contact number
- Image upload for products (`multipart/form-data`, saved to `static/images/`)
- Contact Us form, persisted to the database
- Clean, responsive green-and-white UI (mobile-friendly navbar, cards, forms)
- Clear separation of concerns: **db.py** (SQL/data access) →
  **app.py** (routes/controllers) → **templates/** (views)
- Parameterized queries throughout (protects against SQL injection)

---

## 7. Notes & Simplifications (by design, for a mini project)

- Passwords are stored in **plain text** for simplicity — in a real
  application you would hash them (e.g. with `werkzeug.security.generate_password_hash`).
- No JWT / OAuth — authentication is done with Flask's built-in signed
  session cookies.
- No payment gateway — this is a discovery/contact platform; the actual
  transaction happens off-platform between farmer and consumer (phone call).
- No AI features — all logic is plain CRUD + search.
- `app.run(debug=True)` is for local development only — disable `debug`
  and use a production WSGI server (e.g. Gunicorn) if you deploy this.

---

## 8. Possible Extensions (if you want to go further)

- Password hashing with `werkzeug.security`
- Pagination for the product listing (`LIMIT`/`OFFSET`)
- Order/cart system with order history
- Admin panel to moderate farmers/products/messages
- Deploy to a cloud host (e.g. Render, Railway, PythonAnywhere) with a
  managed MySQL instance

---

## 9. Switching to SQLite (optional, for even simpler local testing)

If you don't want to install MySQL at all, you can swap `db.py` to use
Python's built-in `sqlite3` module instead of PyMySQL — the SQL syntax in
`database/farmer_consumer.sql` is standard enough to adapt with minor
changes (e.g. `AUTO_INCREMENT` → `AUTOINCREMENT`, remove `ENGINE=InnoDB`).
This isn't wired up by default since the original spec calls for MySQL, but
it's a straightforward swap if you'd like a zero-install option.
