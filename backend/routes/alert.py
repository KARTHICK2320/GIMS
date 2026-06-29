from flask import Blueprint, jsonify
from middleware.auth import token_required
import models.product as product_model

alert_bp = Blueprint("alert", __name__)

@alert_bp.route("/critical", methods=["GET"])
@token_required
def get_critical_alerts():
    try:
        products = product_model.find_by_status("critical")
        return jsonify({
            "success": True,
            "data": products
        }), 200
    except Exception as error:
        return jsonify({"success": False, "message": f"Database query failed: {str(error)}"}), 500

@alert_bp.route("/low-stock", methods=["GET"])
@token_required
def get_low_stock_alerts():
    try:
        products = product_model.find_by_status("low-stock")
        return jsonify({
            "success": True,
            "data": products
        }), 200
    except Exception as error:
        return jsonify({"success": False, "message": f"Database query failed: {str(error)}"}), 500

