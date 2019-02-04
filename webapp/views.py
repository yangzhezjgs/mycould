from flask import render_template
from flask import request
from flask import redirect
from flask import Blueprint

from .app import db
from .models import Item

todolist = Blueprint('todolist',__name__)

@todolist.route('/')
def index():
    items = Item.query.all()
    print(items)
    return render_template('index.html', items=items)

@todolist.route('/items/add', methods = ["POST"])
def add():
    content = request.form['content']
    item = Item(content=content)
    db.session.add(item)
    db.session.commit()
    return redirect('/')

@todolist.route('/items/delete/<int:item_id>', methods=["GET"])
def delete(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')

@todolist.route('/items/done/<int:item_id>', methods=["GET"])
def done(item_id):
    item = Item.query.get(item_id)
    item.is_finish = not item.is_finish
    print(item.is_finish)
    db.session.commit()
    return redirect('/')
