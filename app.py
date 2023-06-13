import os
from flask import Flask, render_template, request, url_for, Blueprint
from logging import FileHandler, WARNING
from datetime import datetime
from models import User, Products, db
from dash_board import my_dash_board
from order import customer_order
from cashier import my_cashier
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.register_blueprint(my_dash_board, url_prefix="/admin")
app.register_blueprint(customer_order, url_prefix="/order")
app.register_blueprint(my_cashier, url_prefix="/cashier")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'wtf123456'
app.permanent_session_lifetime = timedelta(hours=6)


file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "dashboard.login_system"

now = datetime.now()

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
