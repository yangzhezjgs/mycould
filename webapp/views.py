from flask import render_template
from flask import request
from flask import redirect
from flask import Blueprint

from .app import db,bootstrap
from .models import Item
from .forms import TextForm

todolist = Blueprint('todolist',__name__)

@todolist.route('/')
def index():
    form = TextForm()
    items = Item.query.all()
    return render_template('index.html', items=items, form=form)

@todolist.route('/items/add', methods = ["POST"])
def add():
    form = TextForm()
    if form.validate_on_submit():
        content = form.text.data
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
