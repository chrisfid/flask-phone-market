from flask import render_template, flash, url_for, redirect, request, abort, Blueprint
from flask_login.utils import login_required
from flask_login import current_user
from market import db
from market.models import Post
from market.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/<int:post_id>')
@login_required
def post_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.forum_page'))
    return render_template('create_update_post.html', form=form, legend='New Post')


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post_page', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_update_post.html', title='Update Post', form=form,
                           legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        # Forbidden route
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted!', category='success')
    return redirect(url_for('main.forum_page'))
