import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider
from werkzeug.exceptions import HTTPException

from config import Config
import db
from limiter import limiter
from routes.auth import auth_bp
from routes.product import product_bp
from routes.dashboard import dashboard_bp
from routes.alert import alert_bp
from routes.report import report_bp

# Custom JSON provider to format datetimes to ISO 8601 strings
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super().default(obj)

def create_app():
    # Verify DB connectivity at startup before booting HTTP server
    db.test_connection()


    app = Flask(__name__)
    
    # Configure custom json provider
    app.json = CustomJSONProvider(app)

    # Configure CORS
    CORS(
        app,
        resources={r"/api/*": {"origins": Config.CORS_ORIGIN}},
        supports_credentials=True
    )

    # Initialize Rate Limiting
    limiter.init_app(app)

    # Register API Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(alert_bp, url_prefix="/api/alerts")
    app.register_blueprint(report_bp, url_prefix="/api/reports")

    # API health check
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "success": True,
            "message": "GIMS Flask API is running"
        }), 200

    # 404 handler
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            "message": "Route not found"
        }), 404

    # Global Exception Handler
    @app.errorhandler(Exception)
    def handle_exception(e):

        # HTTP exceptions (like 405 Method Not Allowed or 400 Bad Request)
        if isinstance(e, HTTPException):
            return jsonify({
                "success": False,
                "message": e.description
            }), e.code

        # Custom user-defined service exceptions
        status_code = getattr(e, "statusCode", 500)
        message = str(e)
        
        # Log unexpected 500 Internal Server Errors
        if status_code == 500:
            app.logger.error(f"Internal Server Error: {message}", exc_info=True)
            message = "Internal Server Error"

        return jsonify({
            "success": False,
            "message": message
        }), status_code

    return app

if __name__ == "__main__":
    app = create_app()
    print(f"Server: GIMS Flask API running on http://localhost:{Config.PORT}")
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
