import os
from flask import Flask, render_template
from .auth import auth  # Keep authentication


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'security.sqlite')
    )

    @app.route('/')
    def home():
        return render_template('home.html')  # Security dashboard

    app.register_blueprint(auth)  # Keep login/register functionality

    from . import db
    db.init_app(app)

    return app
