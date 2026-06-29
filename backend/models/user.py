import db

def find_by_email(email):
    sql = "SELECT id, name, email, password_hash, role, created_at FROM users WHERE email = %s"
    results = db.query(sql, [email])
    return results[0] if results else None

def find_by_id(user_id):
    sql = "SELECT id, name, email, role, created_at FROM users WHERE id = %s"
    results = db.query(sql, [user_id])
    return results[0] if results else None

def create(name, email, password_hash, role="user"):
    sql = "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)"
    result = db.execute(sql, [name, email, password_hash, role])
    return result["last_row_id"]

