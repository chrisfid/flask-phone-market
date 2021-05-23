from operator import pos
import secrets
import os
from PIL import Image
from flask_login.utils import logout_user
from sqlalchemy.orm.query import Query
from wtforms import validators
from market import app
from flask import render_template, redirect, url_for, flash, request, abort
from market.models import Item, User, Post
from market.forms import LoginForm, RegisterForm, PurchaseItemForm, SellItemForm, UpdateAccountForm, PostForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
 
@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form =SellItemForm()
    if request.method == 'POST':
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulations! You have just purchased {p_item_object.name} for {p_item_object.price}$', category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category='danger')
        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Congratulations! You have just sold {s_item_object.name} for {s_item_object.price}$', category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data, 
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account has been created successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('market_page'))
    # If there are no errors from validations
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match. Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))

def save_picture(form_picture) -> str:
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_file_name)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_file_name

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account_page():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email_address = form.email_address.data
        db.session.commit()
        flash(f'Your account has been updated!', category='success')
        return redirect(url_for('account_page'))
    if form.picture.errors:
        for err_msg in form.picture.errors:
            flash(err_msg, category='danger')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email_address.data = current_user.email_address
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', image_file=image_file, form=form)

@app.route('/forum')
@login_required
def forum_page():
    posts = Post.query.all()
    return render_template('forum.html', posts=posts)
 
@app.route('/post/<int:post_id>')
@login_required
def post_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,  content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('forum_page'))
    return render_template('create_post.html', form=form, legend='New Post')

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        # Forbidden route
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('You post has been updated!', category='success')
        return redirect(url_for('post_page', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, 
                            legend='Update Post')

@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        # Forbidden route
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted!', category='success')
    return redirect(url_for('forum_page'))