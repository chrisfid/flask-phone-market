from flask import flash, redirect, url_for, render_template, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from market import db
from market.users.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from market.models import User, Post
from market.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f'Account has been created successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('main.market_page'))
    # If there are no errors from validations
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('main.market_page'))
        else:
            flash('Username and password are not match. Please try again',
                  category='danger')
    return render_template('login.html', form=form)


@users.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('main.home_page'))


@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('main.account_page'))
    if form.picture.errors:
        for err_msg in form.picture.errors:
            flash(err_msg, category='danger')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email_address.data = current_user.email_address
    image_file = url_for(
        'static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', image_file=image_file, form=form)


@users.route('/forum/<string:username>')
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.time_created.desc())\
        .paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return(url_for('main.home_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email_address=form.email_address.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', category='info')
        return redirect(url_for('main.login_page'))
    if form.email_address.errors:
        for err_msg in form.email_address.errors:
            flash(err_msg, category='danger')
    return render_template('reset_request.html', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return(url_for('main.home_page'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', category='warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password1.data
        db.session.commit()
        flash(f'You password has been updated! You are now able to log in.',
              category='success')
        return redirect(url_for('users.login_page'))
    if form.errors != {}:
        flash(f'Passwords do not match.', category='danger')
    return render_template('reset_token.html', form=form)
