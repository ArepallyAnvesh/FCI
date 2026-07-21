"""
db.py
-----
Database access layer for the FCI app. Uses PyMySQL to talk to MySQL.
Every function here opens its own short-lived connection and uses
parameterized queries (%s placeholders) to prevent SQL injection.

This module plays the same role the DAO classes played in the Java
version: model.py holds the "shape" of the data (as plain dicts from
DictCursor), and this file holds all the SQL.
"""

import pymysql
import pymysql.cursors

import config


def get_connection():
    """Opens and returns a new MySQL connection with dict-style rows."""
    return pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


# ======================================================================
# Farmers
# ======================================================================

def create_farmer(name, mobile, email, address, password):
    sql = """INSERT INTO farmers (name, mobile, email, address, password)
             VALUES (%s, %s, %s, %s, %s)"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name, mobile, email, address, password))
            return cur.lastrowid


def farmer_email_exists(email):
    sql = "SELECT farmer_id FROM farmers WHERE email = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (email,))
            return cur.fetchone() is not None


def get_farmer_by_credentials(email, password):
    sql = "SELECT * FROM farmers WHERE email = %s AND password = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (email, password))
            return cur.fetchone()


def get_farmer_by_id(farmer_id):
    sql = "SELECT * FROM farmers WHERE farmer_id = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (farmer_id,))
            return cur.fetchone()


# ======================================================================
# Consumers
# ======================================================================

def create_consumer(name, mobile, email, address, password):
    sql = """INSERT INTO consumers (name, mobile, email, address, password)
             VALUES (%s, %s, %s, %s, %s)"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name, mobile, email, address, password))
            return cur.lastrowid


def consumer_email_exists(email):
    sql = "SELECT consumer_id FROM consumers WHERE email = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (email,))
            return cur.fetchone() is not None


def get_consumer_by_credentials(email, password):
    sql = "SELECT * FROM consumers WHERE email = %s AND password = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (email, password))
            return cur.fetchone()


# ======================================================================
# Products
# ======================================================================

def add_product(farmer_id, product_name, category, price, quantity, description, image_path):
    sql = """INSERT INTO products
             (farmer_id, product_name, category, price, quantity, description, image_path)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (farmer_id, product_name, category, price,
                               quantity, description, image_path))
            return cur.lastrowid


def update_product(product_id, farmer_id, product_name, category, price,
                    quantity, description, image_path):
    sql = """UPDATE products
             SET product_name = %s, category = %s, price = %s, quantity = %s,
                 description = %s, image_path = %s
             WHERE product_id = %s AND farmer_id = %s"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (product_name, category, price, quantity,
                               description, image_path, product_id, farmer_id))
            return cur.rowcount > 0


def delete_product(product_id, farmer_id):
    sql = "DELETE FROM products WHERE product_id = %s AND farmer_id = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (product_id, farmer_id))
            return cur.rowcount > 0


def get_products_by_farmer(farmer_id):
    sql = "SELECT * FROM products WHERE farmer_id = %s ORDER BY created_at DESC"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (farmer_id,))
            return cur.fetchall()


def get_all_products():
    sql = """SELECT p.*, f.name AS farmer_name, f.mobile AS farmer_mobile
             FROM products p JOIN farmers f ON p.farmer_id = f.farmer_id
             ORDER BY p.created_at DESC"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


def search_products(keyword):
    sql = """SELECT p.*, f.name AS farmer_name, f.mobile AS farmer_mobile
             FROM products p JOIN farmers f ON p.farmer_id = f.farmer_id
             WHERE p.product_name LIKE %s OR p.category LIKE %s
             ORDER BY p.created_at DESC"""
    pattern = f"%{keyword}%"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (pattern, pattern))
            return cur.fetchall()


def get_product_by_id(product_id):
    sql = """SELECT p.*, f.name AS farmer_name, f.mobile AS farmer_mobile
             FROM products p JOIN farmers f ON p.farmer_id = f.farmer_id
             WHERE p.product_id = %s"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (product_id,))
            return cur.fetchone()


def get_featured_products(limit=4):
    sql = """SELECT p.*, f.name AS farmer_name, f.mobile AS farmer_mobile
             FROM products p JOIN farmers f ON p.farmer_id = f.farmer_id
             ORDER BY p.created_at DESC LIMIT %s"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()


# ======================================================================
# Contact messages
# ======================================================================

def save_contact_message(name, email, message):
    sql = "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name, email, message))
            return cur.lastrowid
