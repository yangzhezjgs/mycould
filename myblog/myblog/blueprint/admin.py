from flask import Blueprint, redirect, request, render_template, url_for
from flask_login import login_required, current_user

from myblog.models import Post, Category
from myblog.extensions import db
from myblog.forms import PostForm, CategoryForm

admin = Blueprint('admin', __name__)

@admin.route('/manage')
@admin.route('/manage/posts')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('admin/admin.html', pagination=pagination, posts=posts, page=page, index=1)

@admin.route('/manage/categories')
@login_required
def manage_category():
    return render_template('admin/admin.html', index=2)

@admin.route('/delete/post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.manage_post'))

@admin.route('/edit/post/<int:post_id>', methods=['POST','GET'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form, post=post)

@admin.route('/add/post', methods=['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)
    
@admin.route('/edit/category/<int:category_id>', methods=['POST','GET'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        return redirect(url_for('admin.manage_category'))
    form.name.date = category.name
    return render_template('admin/edit_category.html', form=form, category=category)

@admin.route('/delete/category/<int:category_id>', methods=['POST', 'GET'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    category.delete()
    db.session.commit()
    return redirect(url_for('admin.manage_category'))

@admin.route('/add/category/', methods=['GET','POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin.manage_category'))
    return render_template('admin/new_category.html', form=form)


