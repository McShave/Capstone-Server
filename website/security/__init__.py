import os
from flask import Flask, render_template
from .auth import auth  # Keep authentication
from instance import config


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
<<<<<<< HEAD
        SECRET_KEY=config.SECRET,
=======
        SECRET_KEY='dev',
>>>>>>> a3760b3bbc96c29e6bbb428486209781bea4252f
        DATABASE=os.path.join(app.instance_path, 'security.sqlite')
    )

    @app.route('/')
    def home():
        return render_template('home.html')  # Security dashboard

    app.register_blueprint(auth)  # Keep login/register functionality

    from . import db
    db.init_app(app)

    return app
