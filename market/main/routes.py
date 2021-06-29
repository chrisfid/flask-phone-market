from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login.utils import login_required, current_user
from market.models import Item, Post
from market.users.forms import PurchaseItemForm, SellItemForm

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home_page():
    return render_template('home.html')


@main.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(
                    f'Congratulations! You have just purchased {p_item_object.name} for {p_item_object.price}$', category='success')
            else:
                flash(
                    f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category='danger')
        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(
                    f'Congratulations! You have just sold {s_item_object.name} for {s_item_object.price}$', category='success')
            else:
                flash(
                    f"Something went wrong with selling {s_item_object.name}", category='danger')
        return redirect(url_for('main.market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@main.route('/forum')
@login_required
def forum_page():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.time_created.desc()).paginate(page=page, per_page=4)
    return render_template('forum.html', posts=posts)
