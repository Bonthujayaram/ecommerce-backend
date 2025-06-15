import sqlite3
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import json

load_dotenv()

# SQLite connection
sqlite_conn = sqlite3.connect('instance/yourdb.db')
sqlite_cur = sqlite_conn.cursor()

# PostgreSQL connection
database_url = os.environ.get('DATABASE_URL')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

pg_conn = psycopg2.connect(database_url)
pg_cur = pg_conn.cursor()

try:
    # Migrate products
    print("Migrating products...")
    sqlite_cur.execute("SELECT * FROM product")
    products = sqlite_cur.fetchall()
    if products:
        columns = ['id', 'name', 'category', 'price', 'description', 'image_url', 'rating', 'stock_quantity', 'brand']
        query = """
            INSERT INTO product (id, name, category, price, description, image_url, rating, stock_quantity, brand)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                category = EXCLUDED.category,
                price = EXCLUDED.price,
                description = EXCLUDED.description,
                image_url = EXCLUDED.image_url,
                rating = EXCLUDED.rating,
                stock_quantity = EXCLUDED.stock_quantity,
                brand = EXCLUDED.brand
        """
        execute_values(pg_cur, query, products)
        print(f"Migrated {len(products)} products")

    # Migrate users
    print("Migrating users...")
    sqlite_cur.execute("SELECT * FROM user")
    users = sqlite_cur.fetchall()
    if users:
        columns = ['id', 'username', 'email', 'password', 'created_at']
        query = """
            INSERT INTO "user" (id, username, email, password, created_at)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                username = EXCLUDED.username,
                email = EXCLUDED.email,
                password = EXCLUDED.password,
                created_at = EXCLUDED.created_at
        """
        execute_values(pg_cur, query, users)
        print(f"Migrated {len(users)} users")

    # Migrate users profile
    print("Migrating users profile...")
    sqlite_cur.execute("SELECT * FROM users")
    users_profile = sqlite_cur.fetchall()
    if users_profile:
        columns = ['id', 'user_id', 'first_name', 'last_name', 'gender', 'mail', 'phone', 'created_at', 'updated_at']
        query = """
            INSERT INTO users (id, user_id, first_name, last_name, gender, mail, phone, created_at, updated_at)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                user_id = EXCLUDED.user_id,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                gender = EXCLUDED.gender,
                mail = EXCLUDED.mail,
                phone = EXCLUDED.phone,
                updated_at = EXCLUDED.updated_at
        """
        execute_values(pg_cur, query, users_profile)
        print(f"Migrated {len(users_profile)} user profiles")

    # Migrate addresses
    print("Migrating addresses...")
    sqlite_cur.execute("SELECT * FROM addresses")
    addresses = sqlite_cur.fetchall()
    if addresses:
        columns = ['id', 'user_id', 'label', 'name', 'phone', 'address', 'created_at', 'updated_at']
        query = """
            INSERT INTO addresses (id, user_id, label, name, phone, address, created_at, updated_at)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                user_id = EXCLUDED.user_id,
                label = EXCLUDED.label,
                name = EXCLUDED.name,
                phone = EXCLUDED.phone,
                address = EXCLUDED.address,
                updated_at = EXCLUDED.updated_at
        """
        execute_values(pg_cur, query, addresses)
        print(f"Migrated {len(addresses)} addresses")

    # Migrate orders
    print("Migrating orders...")
    sqlite_cur.execute("SELECT * FROM orders")
    orders = sqlite_cur.fetchall()
    if orders:
        columns = ['id', 'user_id', 'total_amount', 'payment_method', 'payment_details', 'status', 'order_date', 'address_id']
        query = """
            INSERT INTO orders (id, user_id, total_amount, payment_method, payment_details, status, order_date, address_id)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                user_id = EXCLUDED.user_id,
                total_amount = EXCLUDED.total_amount,
                payment_method = EXCLUDED.payment_method,
                payment_details = EXCLUDED.payment_details,
                status = EXCLUDED.status,
                order_date = EXCLUDED.order_date,
                address_id = EXCLUDED.address_id
        """
        execute_values(pg_cur, query, orders)
        print(f"Migrated {len(orders)} orders")

    # Migrate order items
    print("Migrating order items...")
    sqlite_cur.execute("SELECT * FROM order_items")
    order_items = sqlite_cur.fetchall()
    if order_items:
        columns = ['id', 'order_id', 'product_id', 'quantity', 'price']
        query = """
            INSERT INTO order_items (id, order_id, product_id, quantity, price)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                order_id = EXCLUDED.order_id,
                product_id = EXCLUDED.product_id,
                quantity = EXCLUDED.quantity,
                price = EXCLUDED.price
        """
        execute_values(pg_cur, query, order_items)
        print(f"Migrated {len(order_items)} order items")

    # Commit all changes
    pg_conn.commit()
    print("Migration completed successfully!")

except Exception as e:
    pg_conn.rollback()
    print(f"Error during migration: {str(e)}")
    raise

finally:
    # Close connections
    sqlite_cur.close()
    sqlite_conn.close()
    pg_cur.close()
    pg_conn.close() 