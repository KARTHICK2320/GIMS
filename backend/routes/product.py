from flask import Blueprint, request, jsonify, g
from middleware.auth import token_required
import models.product as product_model
import models.department as department_model
import models.transaction as transaction_model
import models.log as log_model

product_bp = Blueprint("product", __name__)

def calculate_status(stock):
    stock_num = int(stock)
    if stock_num >= 100:
        return "in-stock"
    elif stock_num >= 21:
        return "low-stock"
    return "critical"

def validate_product_payload(data, is_update=False):
    errors = []
    name = data.get("name", "")
    department_id = data.get("departmentId", "")
    stock = data.get("stock")
    unit = data.get("unit", "Pcs")
    cost = data.get("cost")

    # If it is an update and parameters are missing, we can default to existing values.
    # However, to match express-validator's strict replacement validation, we check all fields.
    if not name or not str(name).strip():
        errors.append({"field": "name", "message": "Product name is required."})
    elif len(str(name)) > 100:
        errors.append({"field": "name", "message": "Product name cannot exceed 100 characters."})

    if not department_id or not str(department_id).strip():
        errors.append({"field": "departmentId", "message": "Department ID is required."})
    elif not department_model.exists(department_id):
        errors.append({"field": "departmentId", "message": f"Department with ID '{department_id}' does not exist."})

    if stock is None:
        errors.append({"field": "stock", "message": "Stock quantity is required."})
    else:
        try:
            stock_val = int(stock)
            if stock_val < 0:
                errors.append({"field": "stock", "message": "Stock must be a non-negative integer."})
        except ValueError:
            errors.append({"field": "stock", "message": "Stock must be an integer."})

    if cost is None:
        errors.append({"field": "cost", "message": "Cost is required."})
    else:
        try:
            cost_val = float(cost)
            if cost_val < 0.0:
                errors.append({"field": "cost", "message": "Cost must be a non-negative decimal."})
        except ValueError:
            errors.append({"field": "cost", "message": "Cost must be a number."})

    if unit and len(str(unit)) > 20:
        errors.append({"field": "unit", "message": "Unit name cannot exceed 20 characters."})

    return errors

@product_bp.route("", methods=["GET"])
def get_products():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        search = request.args.get("search", "")
        department = request.args.get("department", "")
        status = request.args.get("status", "")

        result = product_model.find_all(
            page=page,
            limit=limit,
            search=search,
            department=department,
            status=status
        )

        total_items = result["total"]
        total_pages = (total_items + limit - 1) // limit if total_items > 0 else 0

        return jsonify({
            "success": True,
            "data": result["rows"],
            "pagination": {
                "totalItems": total_items,
                "currentPage": page,
                "totalPages": total_pages,
                "limit": limit
            }
        }), 200
    except Exception as error:
        return jsonify({"success": False, "message": f"Database query failed: {str(error)}"}), 500

@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = product_model.find_by_id(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found."}), 404
    return jsonify({"success": True, "data": product}), 200

@product_bp.route("", methods=["POST"])
@token_required
def create_product():
    data = request.get_json() or {}
    
    # Input validation
    errors = validate_product_payload(data)
    if errors:
        return jsonify({"success": False, "message": "Validation failed.", "errors": errors}), 400

    try:
        name = data.get("name").strip()
        department_id = data.get("departmentId").strip()
        stock = int(data.get("stock"))
        unit = data.get("unit", "Pcs").strip()
        cost = float(data.get("cost"))
        user_id = g.user["id"]

        # Calculate status server-side
        status = calculate_status(stock)

        # Create product in database
        product_id = product_model.create(name, department_id, stock, unit, cost, status)

        # Write initial transaction ledger
        transaction_model.create(
            product_id=product_id,
            change_type="adjustment",
            quantity_change=stock,
            stock_after=stock
        )

        # Write activity log
        log_model.create_log(
            user_id=user_id,
            action="PRODUCT_CREATE",
            details=f"Product '{name}' created with stock {stock} ({status}) and cost {cost:.2f}"
        )

        created_product = product_model.find_by_id(product_id)
        return jsonify({
            "success": True,
            "message": "Product created successfully.",
            "data": created_product
        }), 201

    except Exception as error:
        return jsonify({"success": False, "message": f"Internal Server Error: {str(error)}"}), 500

@product_bp.route("/<int:product_id>", methods=["PUT"])
@token_required
def update_product(product_id):
    current_product = product_model.find_by_id(product_id)
    if not current_product:
        return jsonify({"success": False, "message": "Product not found."}), 404

    data = request.get_json() or {}
    
    # Validate payload
    errors = validate_product_payload(data, is_update=True)
    if errors:
        return jsonify({"success": False, "message": "Validation failed.", "errors": errors}), 400

    try:
        name = data.get("name").strip()
        department_id = data.get("departmentId").strip()
        new_stock = int(data.get("stock"))
        unit = data.get("unit", "Pcs").strip()
        cost = float(data.get("cost"))
        user_id = g.user["id"]
        
        old_stock = int(current_product["stock"])
        status = calculate_status(new_stock)

        # Execute DB update
        product_model.update(product_id, name, department_id, new_stock, unit, cost, status)

        # Check if stock changed to write transaction ledger
        if old_stock != new_stock:
            delta = new_stock - old_stock
            change_type = "restock" if delta > 0 else "sale"
            
            # Log delta transaction
            transaction_model.create(
                product_id=product_id,
                change_type=change_type,
                quantity_change=delta,
                stock_after=new_stock
            )
            
            # Log activity with stock changes
            log_model.create_log(
                user_id=user_id,
                action="PRODUCT_UPDATE",
                details=f"Product '{current_product['name']}' stock updated: {old_stock} -> {new_stock} (delta: {delta:+d})"
            )
        else:
            # Log activity without stock changes
            log_model.create_log(
                user_id=user_id,
                action="PRODUCT_UPDATE",
                details=f"Product '{current_product['name']}' info updated (no stock changes)"
            )

        updated_product = product_model.find_by_id(product_id)
        return jsonify({
            "success": True,
            "message": "Product updated successfully.",
            "data": updated_product
        }), 200

    except Exception as error:
        return jsonify({"success": False, "message": f"Internal Server Error: {str(error)}"}), 500

@product_bp.route("/<int:product_id>", methods=["DELETE"])
@token_required
def delete_product(product_id):
    product = product_model.find_by_id(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found."}), 404

    try:
        user_id = g.user["id"]
        deleted = product_model.remove(product_id)
        
        if not deleted:
            return jsonify({"success": False, "message": "Failed to delete product."}), 500

        # Log deletion
        log_model.create_log(
            user_id=user_id,
            action="PRODUCT_DELETE",
            details=f"Product '{product['name']}' (ID: {product_id}) deleted"
        )

        return jsonify({
            "success": True,
            "message": "Product deleted successfully."
        }), 200

    except Exception as error:
        return jsonify({"success": False, "message": f"Internal Server Error: {str(error)}"}), 500
