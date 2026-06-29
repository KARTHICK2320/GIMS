import db

def find_by_id(product_id):
    sql = """
        SELECT p.*, d.name as department_name 
        FROM products p 
        JOIN departments d ON p.department_id = d.id 
        WHERE p.id = %s
    """
    results = db.query(sql, [product_id])
    return results[0] if results else None

def find_by_status(status):
    sql = """
        SELECT p.id, p.name, p.department_id, p.stock, p.unit, p.cost, p.status, p.created_at, d.name as department_name 
        FROM products p 
        JOIN departments d ON p.department_id = d.id 
        WHERE p.status = %s 
        ORDER BY p.name ASC
    """
    return db.query(sql, [status])

def create(name, department_id, stock, unit, cost, status):
    sql = """
        INSERT INTO products (name, department_id, stock, unit, cost, status) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    result = db.execute(sql, [name, department_id, stock, unit, cost, status])
    return result["last_row_id"]

def update(product_id, name, department_id, stock, unit, cost, status):
    sql = """
        UPDATE products 
        SET name = %s, department_id = %s, stock = %s, unit = %s, cost = %s, status = %s 
        WHERE id = %s
    """
    db.execute(sql, [name, department_id, stock, unit, cost, status, product_id])
    return True

def remove(product_id):
    sql = "DELETE FROM products WHERE id = %s"
    result = db.execute(sql, [product_id])
    return result["affected_rows"] > 0


# Find all products with pagination and filters
def find_all(page=1, limit=10, search="", department="", status=""):
    sql = """
        SELECT p.id, p.name, p.department_id, p.stock, p.unit, p.cost, p.status, p.created_at, d.name as department_name 
        FROM products p 
        JOIN departments d ON p.department_id = d.id
    """
    count_sql = """
        SELECT COUNT(*) as total 
        FROM products p 
        JOIN departments d ON p.department_id = d.id
    """
    
    where_clauses = []
    params = []

    # Case-insensitive text search matching product name
    if search:
        where_clauses.append("p.name LIKE %s")
        params.append(f"%{search}%")

    # Category filter by department slug
    if department:
        where_clauses.append("p.department_id = %s")
        params.append(department)

    # Status filter (in-stock, low-stock, critical)
    if status:
        where_clauses.append("p.status = %s")
        params.append(status)

    if where_clauses:
        where_str = " WHERE " + " AND ".join(where_clauses)
        sql += where_str
        count_sql += where_str

    # Execute total counts first
    count_results = db.query(count_sql, params)
    total = count_results[0]["total"] if count_results else 0

    # Sort descending by ID, paginate with limit and offset
    sql += " ORDER BY p.id DESC LIMIT %s OFFSET %s"
    offset = (page - 1) * limit
    
    query_params = params + [int(limit), int(offset)]
    rows = db.query(sql, query_params)

    return {
        "total": total,
        "rows": rows
    }

def get_summary_general():
    sql = "SELECT COUNT(*) as totalProducts, IFNULL(SUM(stock * cost), 0.00) as totalValue FROM products"
    results = db.query(sql)
    if results:
        # Cast values properly
        return {
            "totalProducts": int(results[0]["totalProducts"]),
            "totalValue": float(results[0]["totalValue"])
        }
    return {"totalProducts": 0, "totalValue": 0.0}

def get_summary_by_status():
    sql = "SELECT status, COUNT(*) as count FROM products GROUP BY status"
    return db.query(sql)

def get_summary_by_department():
    sql = """
        SELECT d.id as department_id, d.name as department_name, d.icon, d.color, 
               COUNT(p.id) as productCount, IFNULL(SUM(p.stock * p.cost), 0.00) as totalValue 
        FROM departments d 
        LEFT JOIN products p ON d.id = p.department_id 
        GROUP BY d.id, d.name, d.icon, d.color
    """
    return db.query(sql)

