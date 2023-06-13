import os
import os.path
from flask import Flask, render_template, request, url_for, Blueprint, flash, redirect, session
from logging import FileHandler, WARNING
from datetime import datetime
from models import User, Products, Order, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField, IntegerField, DateTimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from datetime import timedelta
from collections import defaultdict


app = Flask(__name__)
customer_order = Blueprint("order", "order", static_folder="static", template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ALL_TABLE = 10


def mergerDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


def collectOrder(pid, order, amount, price, dc_price):
    table = session['order_table']
    order_list = {'menu': pid, 'order': order, 'amount': amount, 'price': price, 'discount_price': dc_price}
    order_list['table'] = table
    return order_list


@customer_order.route('/<int:table>', methods=["POST", "GET"])
def incoming_order(table):
    try:
        if 0 < table <= ALL_TABLE:
            session['order_table'] = table
            all_products = Products.query.all()
            return render_template("order.html", products=all_products)
        else:
            return render_template("table_not_found.html")

    except Exception as e:
        print(e)
        return redirect(url_for("order.incoming_order"))


@customer_order.route('/confirm_order', methods=["POST", "GET"])
def confirm_order():
    try:
        if request.method == 'POST':
            table = session['order_table']
            menu = request.form.getlist('menu[]')
            order = []
            set_price = []
            dc_price = []
            for item in menu:
                order_menu = Products.query.filter_by(product_id=item).first()
                order.append(order_menu.product_name)
                set_price.append(order_menu.set_price)
                dc_price.append(order_menu.selling_price)
            number = request.form.getlist('order_number[]')
            amount = []
            for i in number:
                if i == '':
                    i = 0
                else:
                    i = int(i)
                amount.append(i)
            recieve = [*map(collectOrder, menu, order, amount, set_price, dc_price)]

            return render_template("confirm_order.html", incoming_order=recieve)

    except Exception as e:
        print(e)
        return redirect(url_for("incoming_order"))


@customer_order.route('/summary_order', methods=["POST", "GET"])
def summary_order():
    try:
        if request.method == 'POST':
            table = session['order_table']
            menu = request.form.getlist('menu[]')
            order = request.form.getlist('order[]')
            amount = request.form.getlist('amount[]')
            set_price = request.form.getlist('set_price[]')
            dc_price = request.form.getlist('dc_price[]')
            this_order = [*map(collectOrder, menu, order, amount, set_price, dc_price)]

            if 'order_menu' not in session:
                session['order_menu'] = this_order
            elif 'order_menu' and 'order_table' in session:
                for item in this_order:
                    session['order_menu'].append(item)
            print(session['order_menu'])

        for order in session['order_menu']:
            old_quantity = Products.query.filter_by(product_id=order['menu']).first()
            new_quantity = int(old_quantity.amount) - int(order['amount'])
            old_quantity.amount = new_quantity
            db.session.commit()

            new_order = Order(
                table_no=order['table'],
                time=datetime.now(),
                order=order['order'],
                amount=order['amount'],
                set_price=order['price'],
                dc_price=order['discount_price']
            )
            db.session.add(new_order)
            db.session.commit()
        session.pop('order_menu', None)

        return render_template("summary.html")

    except Exception as e:
        print(e)
        return redirect(url_for("order.incoming_order", table=session['order_table']))


