import click
from flask import Flask
from myblog.extensions import db, bootstrap, login_manager, ckeditor
from myblog.setting import Config
from myblog.models import Admin, Post, Category
from myblog.blueprint.blog import blog
from myblog.blueprint.auth import auth
from myblog.blueprint.admin import admin

def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

def register_commands(app):
    @app.cli.command()
    def faker():
        from myblog.fake import faker_category, faker_posts, faker_admin
        db.drop_all()
        db.create_all()
        
        faker_category()
        faker_posts()
        faker_admin()
        click.echo("done")

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category)



def register_template_context(app):
    @app.context_processor
    def make_template_context():
        categories = Category.query.order_by(Category.name).all()
        return dict(categories=categories)

def register_blueprint(app):
    app.register_blueprint(blog)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    register_extensions(app)
    register_commands(app)
    register_shell_context(app)
    register_blueprint(app)
    register_template_context(app)

    return app