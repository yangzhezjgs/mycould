from datetime import datetime
from sqlalchemy import Column

from flask_login import UserMixin

from myblog.extensions import db

class Admin(db.Model, UserMixin):
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(20))
    password = Column(db.String(20))
    

class Post(db.Model):
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(50))
    body = Column(db.Text)
    timestamp = Column(db.DateTime, default=datetime.utcnow)
    category_id = Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship('Category', back_populates='posts')


class Category(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(20), unique=True)
    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)


    