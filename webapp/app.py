from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from .config import Config

db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY']='yz' 
    db.init_app(app)
    bootstrap.init_app(app)
    from .views import todolist
    app.register_blueprint(todolist)
    return app
