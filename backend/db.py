import os
import sys
import sqlite3
import datetime

DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "gims.db"))

# Custom parser to read SQLite timestamps back as Python datetime objects
def convert_datetime(val):
    val_str = val.decode("utf-8")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.datetime.strptime(val_str, fmt)
        except ValueError:
            continue
    return val_str

# Register adapters and converters
sqlite3.register_adapter(datetime.datetime, lambda val: val.isoformat())
sqlite3.register_adapter(datetime.date, lambda val: val.isoformat())
sqlite3.register_converter("timestamp", convert_datetime)
sqlite3.register_converter("TIMESTAMP", convert_datetime)

def get_connection():
    conn = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("PRAGMA foreign_keys = ON;")
    # Map row columns to dict keys
    conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
    return conn

def init_db():

    schema = """
    CREATE TABLE IF NOT EXISTS departments (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      icon TEXT,
      color TEXT
    );

    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      role TEXT CHECK(role IN ('admin', 'user')) DEFAULT 'user',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS products (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      department_id TEXT NOT NULL,
      stock INTEGER NOT NULL DEFAULT 0,
      unit TEXT NOT NULL DEFAULT 'Pcs',
      cost REAL NOT NULL DEFAULT 0.00,
      status TEXT CHECK(status IN ('in-stock', 'low-stock', 'critical')) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (department_id) REFERENCES departments(id)
    );

    CREATE TABLE IF NOT EXISTS inventory_transactions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      product_id INTEGER NOT NULL,
      change_type TEXT CHECK(change_type IN ('adjustment', 'purchase', 'sale', 'restock')) NOT NULL,
      quantity_change INTEGER NOT NULL,
      stock_after INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS activity_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NULL,
      action TEXT NOT NULL,
      details TEXT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    );

    CREATE INDEX IF NOT EXISTS idx_products_status ON products (status);
    CREATE INDEX IF NOT EXISTS idx_products_dept ON products (department_id);
    CREATE INDEX IF NOT EXISTS idx_transactions_product ON inventory_transactions (product_id);
    CREATE INDEX IF NOT EXISTS idx_logs_user ON activity_logs (user_id);

    -- Seed department data
    INSERT OR IGNORE INTO departments (id, name, icon, color) VALUES
    ('grocery', 'Grocery', '🛒', '#3B82F6'),
    ('fruits-vegetables', 'Fruits & Vegetables', '🥬', '#22C55E'),
    ('dairy', 'Dairy Products', '🧀', '#EAB308'),
    ('beverages', 'Beverages', '🥤', '#EF4444'),
    ('bakery', 'Bakery', '📦', '#F97316'),
    ('household', 'Household', '🏠', '#8B5CF6');
    """
    conn = get_connection()
    try:
        conn.executescript(schema)
        conn.commit()
        
        # Seed initial products if the table is empty
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM products")
        if cursor.fetchone()["count"] == 0:
            products_seed = """
            INSERT INTO products (id, name, department_id, stock, unit, cost, status) VALUES
            (1, 'Rice', 'grocery', 200, 'Nos', 500000, 'in-stock'),
            (2, 'Paste', 'grocery', 50, 'Nos', 2000, 'low-stock'),
            (3, 'Shampoo', 'grocery', 200, 'Nos', 500000, 'critical'),
            (4, 'Sugar', 'grocery', 47, 'Kg', 12000, 'low-stock'),
            (5, 'Tea Powder', 'grocery', 34, 'Kg', 8500, 'low-stock'),
            (6, 'Soap', 'grocery', 124, 'Pcs', 6200, 'in-stock'),
            (7, 'Soft Drinks', 'beverages', 141, 'Nos', 14100, 'in-stock'),
            (8, 'Milk', 'dairy', 80, 'Ltr', 4000, 'low-stock'),
            (9, 'Cheese', 'dairy', 25, 'Kg', 12500, 'low-stock'),
            (10, 'Apples', 'fruits-vegetables', 50, 'Kg', 10000, 'in-stock'),
            (11, 'Tomatoes', 'fruits-vegetables', 30, 'Kg', 3000, 'low-stock'),
            (12, 'Onions', 'fruits-vegetables', 100, 'Kg', 5000, 'in-stock'),
            (13, 'Bread', 'bakery', 60, 'Pcs', 1800, 'low-stock'),
            (14, 'Cake', 'bakery', 15, 'Pcs', 7500, 'critical'),
            (15, 'Butter', 'dairy', 40, 'Pcs', 3200, 'low-stock'),
            (16, 'Juice', 'beverages', 90, 'Nos', 9000, 'in-stock'),
            (17, 'Water', 'beverages', 200, 'Nos', 2000, 'in-stock'),
            (18, 'Detergent', 'household', 75, 'Pcs', 7500, 'low-stock'),
            (19, 'Mop', 'household', 10, 'Pcs', 3000, 'critical'),
            (20, 'Broom', 'household', 20, 'Pcs', 1600, 'low-stock'),
            (21, 'Floor Cleaner', 'household', 45, 'Nos', 4500, 'low-stock');
            """
            cursor.executescript(products_seed)
            conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Database: Schema initialization failed: {e}")
        sys.exit(1)
    finally:
        conn.close()

def test_connection():
    try:
        conn = get_connection()
        conn.execute("SELECT 1").close()
        conn.close()
        print(f"Database: SQLite connected successfully at {DB_FILE}")
        init_db()
    except Exception as error:
        print(f"Database: SQLite connection failed: {error}")
        sys.exit(1)

def query(sql, params=None):
    sql = sql.replace("%s", "?")
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        raise e
    finally:
        conn.close()

def execute(sql, params=None):
    sql = sql.replace("%s", "?")
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        last_id = cursor.lastrowid
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return {"affected_rows": affected, "last_row_id": last_id}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

