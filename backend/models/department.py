import db

def exists(department_id):
    sql = "SELECT 1 FROM departments WHERE id = %s"
    results = db.query(sql, [department_id])
    return len(results) > 0

def get_all():
    sql = "SELECT id, name, icon, color FROM departments"
    return db.query(sql)

