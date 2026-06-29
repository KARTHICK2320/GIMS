import db

def create(product_id, change_type, quantity_change, stock_after):
    sql = """
        INSERT INTO inventory_transactions 
        (product_id, change_type, quantity_change, stock_after) 
        VALUES (%s, %s, %s, %s)
    """
    result = db.execute(sql, [product_id, change_type, quantity_change, stock_after])
    return result["last_row_id"]

def get_by_product_id(product_id):
    sql = """
        SELECT id, product_id, change_type, quantity_change, stock_after, created_at 
        FROM inventory_transactions 
        WHERE product_id = %s 
        ORDER BY created_at DESC
    """
    return db.query(sql, [product_id])

