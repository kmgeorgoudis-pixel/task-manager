from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

    # ✅ Ρύθμιση για uploads — ΜΕΣΑ στη create_app()
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User
    from .routes import main
    app.register_blueprint(main)

    # Automatically create database tables
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
