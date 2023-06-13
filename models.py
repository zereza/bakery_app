from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean)


class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    catagory = db.Column(db.String(80), nullable=False)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    product_name_th = db.Column(db.String(100), unique=True, nullable=False)
    set_price = db.Column(db.Integer, nullable=False)
    images_url = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    selling_price = db.Column(db.Integer)
    new_product = db.Column(db.Boolean)
    recommended = db.Column(db.Boolean)

    def __repr__(self):
        return '<Products %r>' % self.product_name


class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    table_no = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    order = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    set_price = db.Column(db.Integer, nullable=False)
    dc_price = db.Column(db.Integer, default=set_price)
    show_order = db.Column(db.Boolean, default=True)
    paid_status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Order %r>' % self.table_no

