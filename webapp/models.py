from datetime import datetime

from .app import db

from sqlalchemy import Column

class Item(db.Model):
    __tables__ = 'items'

    id = Column(db.Integer, primary_key = True)
    content = Column(db.String(1024), nullable=False)
    create_time = Column(db.DateTime, default=datetime.now())
    is_finish = Column(db.Boolean, default = False)


