import db

def create_log(user_id=None, action="", details=None):
    sql = "INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)"
    result = db.execute(sql, [user_id, action, details])
    return result["last_row_id"]

def get_recent(limit=10):
    sql = """
        SELECT l.id, l.action, l.details, l.created_at, u.name as user_name 
        FROM activity_logs l
        LEFT JOIN users u ON l.user_id = u.id
        ORDER BY l.created_at DESC
        LIMIT %s
    """
    return db.query(sql, [limit])

