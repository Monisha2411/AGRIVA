
import os
from flask import Flask, render_template, jsonify
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

from config import Config
from models import db
from models.user import User

# Import Blueprints
from routes.auth import auth_bp, bcrypt, mail
from routes.dashboard import dashboard_bp
from routes.chatbot import chatbot_bp
from routes.prediction import prediction_bp
from routes.recommendation import recommendation_bp
from routes.marketplace import marketplace_bp
from routes.schemes import schemes_bp
from routes.roadmap import roadmap_bp
from routes.fertilizer import fertilizer_bp
from routes.labour import labour_bp
from routes.shop import shop_bp
from routes.gov_mitra import gov_mitra_bp
from routes.education import education_bp
from routes.goat import goat_bp
from routes.cooler import cooler_bp
from routes.vision import vision_bp


def create_app():
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app.config.from_object(Config)

    # Database initialization
    db.init_app(app)

    # Authentication initialization
    bcrypt.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Mail initialization
    mail.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(marketplace_bp)
    app.register_blueprint(schemes_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(fertilizer_bp)
    app.register_blueprint(labour_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(gov_mitra_bp)
    app.register_blueprint(education_bp)
    app.register_blueprint(goat_bp)
    app.register_blueprint(cooler_bp)
    app.register_blueprint(vision_bp)

    # Create required directories
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database'),
            exist_ok=True
        )
    except OSError as e:
        app.logger.warning("Directory creation skipped: %s", e)

    # Home page
    @app.route('/')
    def index():
        return render_template('index.html')

    # Render health check
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'healthy',
            'application': 'AGRIVA'
        }), 200

    # Favicon
    @app.route('/favicon.ico')
    def favicon():
        return '', 204

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template('500.html'), 500

    return app


# Create Flask application
app = create_app()


def initialize_database():
    """Initialize database tables and synchronize existing columns."""

    with app.app_context():
        from sqlalchemy import text

        try:
            print("[AGRIVA] Establishing database connection...")

            from models.marketplace import CropListing
            from models.prediction import YieldPrediction, ChatHistory
            from models.scheme import GovernmentScheme, SchemeApplication
            from models.labour import LabourWorker
            from models.shop import (
                Shop, Product, Supplier, Sale, SaleItem,
                AutoOrder, ShopNotification, CustomerOrder
            )

            db.create_all()
            print("[AGRIVA] Database tables synchronized.")

            # Database column migrations
            migrations = [
                ("shop_products", "image", "VARCHAR(255)"),
                ("shops", "partner_name", "VARCHAR(150)"),
                ("shops", "partner_details", "TEXT"),
                ("customer_orders", "tracking_id", "VARCHAR(50)"),
                ("labour_workers", "profile_pic", "VARCHAR(255)"),
                ("labour_workers", "aadhaar_pic", "VARCHAR(255)"),
                ("labour_workers", "is_verified", "BOOLEAN DEFAULT FALSE"),
                ("labour_workers", "address", "VARCHAR(255)")
            ]

            for table, column, data_type in migrations:
                try:
                    db.session.execute(
                        text(
                            f"ALTER TABLE {table} "
                            f"ADD COLUMN {column} {data_type}"
                        )
                    )
                    db.session.commit()
                    print(f"[AGRIVA] Added column {table}.{column}")

                except Exception:
                    db.session.rollback()

            print("[AGRIVA] Database synchronization completed.")

        except Exception as e:
            db.session.rollback()
            app.logger.exception(
                "Database initialization encountered an error: %s", e
            )


# Initialize database
initialize_database()


# Security headers
@app.after_request
def add_security_headers(response):

    if app.debug:
        return response

    response.headers['Content-Security-Policy'] = (
        "default-src 'self' http: https:; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' http: https:; "
        "style-src 'self' 'unsafe-inline' http: https:; "
        "img-src 'self' data: http: https:; "
        "font-src 'self' data: http: https:; "
        "frame-src 'self' http: https:; "
        "connect-src 'self' http: https:;"
    )

    response.headers['Strict-Transport-Security'] = (
        'max-age=31536000; includeSubDomains'
    )

    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    return response


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=debug_mode
    )
