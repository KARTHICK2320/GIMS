from flask import Blueprint, jsonify, request
from middleware.auth import token_required
import models.product as product_model
import models.log as log_model

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/summary", methods=["GET"])
@token_required
def get_summary():
    try:
        general = product_model.get_summary_general()
        status_rows = product_model.get_summary_by_status()
        dept_rows = product_model.get_summary_by_department()

        # Parse status counts, ensuring all statuses default to 0
        status_counts = {
            "in-stock": 0,
            "low-stock": 0,
            "critical": 0
        }
        for row in status_rows:
            status = row.get("status")
            if status in status_counts:
                status_counts[status] = int(row["count"])

        # Format departments, transforming decimals/integers appropriately
        departments = []
        for row in dept_rows:
            departments.append({
                "id": row["department_id"],
                "name": row["department_name"],
                "icon": row["icon"],
                "color": row["color"],
                "productCount": int(row["productCount"]),
                "totalValue": float(row["totalValue"])
            })

        return jsonify({
            "success": True,
            "data": {
                "totalProducts": int(general["totalProducts"]),
                "totalValue": float(general["totalValue"]),
                "statusCounts": status_counts,
                "departments": departments
            }
        }), 200

    except Exception as error:
        return jsonify({"success": False, "message": f"Database query failed: {str(error)}"}), 500

@dashboard_bp.route("/recent-activity", methods=["GET"])
@token_required
def get_recent_activity():
    try:
        limit = int(request.args.get("limit", 10))
        logs = log_model.get_recent(limit)

        # Convert datetime objects to ISO strings for JSON serialization
        formatted_logs = []
        for log in logs:
            formatted_logs.append({
                "id": log["id"],
                "action": log["action"],
                "details": log["details"],
                "createdAt": log["created_at"].isoformat() if log["created_at"] else None,
                "userName": log["user_name"] or "System"
            })

        return jsonify({
            "success": True,
            "data": formatted_logs
        }), 200

    except Exception as error:
        return jsonify({"success": False, "message": f"Database query failed: {str(error)}"}), 500

