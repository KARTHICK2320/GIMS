from flask import Blueprint, jsonify
from middleware.auth import token_required
import models.product as product_model

report_bp = Blueprint("report", __name__)

@report_bp.route("/inventory-value", methods=["GET"])
@token_required
def get_inventory_value_report():
    try:
        dept_rows = product_model.get_summary_by_department()
        report_data = []
        for row in dept_rows:
            report_data.append({
                "departmentId": row["department_id"],
                "departmentName": row["department_name"],
                "productCount": int(row["productCount"]),
                "totalValue": float(row["totalValue"])
            })
        return jsonify({
            "success": True,
            "data": report_data
        }), 200
    except Exception as error:
        return jsonify({"success": False, "message": f"Database query failed: {str(error)}"}), 500

@report_bp.route("/stock-distribution", methods=["GET"])
@token_required
def get_stock_distribution_report():
    try:
        status_rows = product_model.get_summary_by_status()
        
        status_counts = {
            "in-stock": 0,
            "low-stock": 0,
            "critical": 0
        }
        for row in status_rows:
            status = row.get("status")
            if status in status_counts:
                status_counts[status] = int(row["count"])
                
        return jsonify({
            "success": True,
            "data": status_counts
        }), 200
    except Exception as error:
        return jsonify({"success": False, "message": f"Database query failed: {str(error)}"}), 500

@report_bp.route("/summary", methods=["GET"])
@token_required
def get_combined_report():
    try:
        # Fetch department value breakdown
        dept_rows = product_model.get_summary_by_department()
        dept_data = []
        total_value = 0.0
        for row in dept_rows:
            val = float(row["totalValue"])
            total_value += val
            dept_data.append({
                "departmentId": row["department_id"],
                "departmentName": row["department_name"],
                "productCount": int(row["productCount"]),
                "totalValue": val
            })

        # Fetch status distribution
        status_rows = product_model.get_summary_by_status()
        status_counts = {
            "in-stock": 0,
            "low-stock": 0,
            "critical": 0
        }
        for row in status_rows:
            status = row.get("status")
            if status in status_counts:
                status_counts[status] = int(row["count"])

        return jsonify({
            "success": True,
            "data": {
                "totalInventoryValue": total_value,
                "departmentBreakdown": dept_data,
                "statusDistribution": status_counts
            }
        }), 200
    except Exception as error:
        return jsonify({"success": False, "message": f"Database query failed: {str(error)}"}), 500

