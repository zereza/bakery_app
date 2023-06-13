import os
import os.path
from flask import Flask, render_template, request, url_for, Blueprint, flash, redirect
from logging import FileHandler, WARNING
from datetime import datetime
from models import User, Products, Order, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField, IntegerField, DateTimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt


UPLOAD_FOLDER = './static/upload'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
my_dash_board = Blueprint("dashboard", "dashboard", static_folder="static", template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

bcrypt = Bcrypt(app)


class Product_form(FlaskForm):
    catagory = SelectField(label='Catagory',
                           choices=[('Dessert', 'Dessert'), ('Beverages', 'Beverages'), ('Milk', 'Milk'),
                                    ('Other', 'Other'),
                                    ('Promotion', 'Promotion')], validators=[DataRequired()])
    product_name = StringField(label='Product Name',
                               validators=[DataRequired()])
    product_name_th = StringField(label='Thai Name', validators=[DataRequired()])
    price = IntegerField(label='Price', validators=[DataRequired()])
    amount = IntegerField(label='Amount', validators=[DataRequired()])
    selling_price = IntegerField(label='Promotion Price')
    new = BooleanField(label='New Product')
    recommended = BooleanField(label='Recommended')


class AdminForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=5, max=20)], render_kw={"placeholder": "Password"})
    is_admin = BooleanField(render_kw={"placeholder": "Admin"})
    submit = SubmitField("Login")


@my_dash_board.route("/register", methods=["POST", "GET"])
def register():
    register_form = AdminForm()
    if register_form.validate_on_submit():
        if User.query.filter_by(username=register_form.username.data).first():
            flash("ชื่อนี้ใช้ลงทะเบียนแล้ว")
            return redirect(url_for("dashboard.register"))
        else:
            hash_password = bcrypt.generate_password_hash(register_form.password.data)
            username = register_form.username.data
            is_admin = register_form.is_admin.data
            new_user = User(
                username=username,
                password=hash_password,
                admin=is_admin
            )
            db.session.add(new_user)
            db.session.commit()
            flash(f"เพิ่มผู้ใช้งาน {username} แล้ว!!")
            return redirect(url_for("dashboard.register"))
    return render_template("register.html", form=register_form)


@my_dash_board.route("/login", methods=["POST", "GET"])
def login_system():
    login_form = AdminForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user)
                return redirect(url_for("dashboard.dashboard1"))

    return render_template("login.html", form=login_form)


@my_dash_board.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard1():
    product = Products.query.all()
    return render_template("dashboard.html", all_product=product)


@my_dash_board.route("/upload", methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        flash("ได้เพิ่มรูปภาพสินค้าแล้ว")
        return redirect(url_for('dashboard.dashboard1'))
    return render_template('upload.html')


@my_dash_board.route("/add", methods=['GET', 'POST'])
@login_required
def add_product():
    to_add_product = Product_form()
    try:
        if to_add_product.validate_on_submit():
            catagory = to_add_product.catagory.data
            name = to_add_product.product_name.data
            name_th = to_add_product.product_name_th.data
            price = to_add_product.price.data
            amount = to_add_product.amount.data
            date = datetime.now()
            selling_price = to_add_product.price.data
            if to_add_product.new.data:
                new = True
            else:
                new = False
            if to_add_product.recommended.data:
                recommended = True
            else:
                recommended = False

            new_item = Products(
                catagory=catagory,
                product_name=name,
                product_name_th=name_th,
                set_price=price,
                images_url='bluecheese.jpg',
                amount=amount,
                last_modified=date,
                selling_price=selling_price,
                new_product=new,
                recommended=recommended
            )
            db.session.add(new_item)
            db.session.commit()
            flash(f"เพิ่มสินค้า {name} แล้ว", "info")
    except ValueError:
        return redirect(url_for('dashboard.dashboard1'))
    except TypeError:
        return redirect(url_for('dashboard.dashboard1'))
    except KeyError:
        return redirect(url_for('dashboard.dashboard1'))
    return render_template("add.html", form=to_add_product)


@my_dash_board.route("/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_product(id):
    product_to_update = Products.query.filter_by(product_id=id).first()
    update_form = Product_form()
    try:
        if update_form.validate_on_submit():
            product_to_update.catagory = update_form.catagory.data
            product_to_update.product_name = update_form.product_name.data
            product_to_update.product_name_th = update_form.product_name_th.data
            product_to_update.price = update_form.price.data
            product_to_update.amount = update_form.amount.data
            product_to_update.last_modified = datetime.now()
            product_to_update.promotion_price = update_form.selling_price.data
            if update_form.new.data:
                product_to_update.new_product = True
            else:
                product_to_update.new_product = False
            if update_form.recommended.data:
                product_to_update.recommended = True
            else:
                product_to_update.recommended = False
            db.session.commit()
            flash(f"เปลี่ยนแปลงข้อมูลสินค้า {product_to_update.product_name} แล้ว", "info")
            return redirect(url_for('dashboard.dashboard1'))
    except ValueError:
        return redirect(url_for('dashboard.dashboard1'))
    except TypeError:
        return redirect(url_for('dashboard.dashboard1'))
    except KeyError:
        return redirect(url_for('dashboard.dashboard1'))
    return render_template("update_product.html", previous=product_to_update, form=update_form)


@my_dash_board.route("/edit_selling_amount/<int:id>", methods=["POST", "GET"])
@login_required
def edit_amount(id):
    to_edit = Products.query.filter_by(product_id=id).first()
    current_amount = to_edit.amount
    if request.method == "POST":
        new_amount = request.form.get("quantity")
        to_edit.amount = new_amount
        db.session.commit()
        flash(f"เปลี่ยนแปลงจำนวนสินค้า {to_edit.product_name} จาก {current_amount} เป็น {new_amount} ชิ้นแล้ว")
        return redirect(url_for("dashboard.dashboard1"))
    return render_template("edit_selling_amount.html", data=to_edit)


@my_dash_board.route("/delete/<int:id>", methods=["POST", "GET"])
@login_required
def delete(id):
    to_delete = Products.query.filter_by(product_id=id).first()
    db.session.delete(to_delete)
    db.session.commit()
    flash(f"Product {to_delete.product_name} has been deleted!!", "info")
    return redirect(url_for("dashboard.dashboard1"))


@my_dash_board.route("/select_image/<int:id>", methods=["POST", "GET"])
@login_required
def select_image(id):
    if os.path.exists(UPLOAD_FOLDER):
        files = os.listdir(UPLOAD_FOLDER)

    url_to_change = Products.query.filter_by(product_id=id).first()
    if request.method == 'POST':
        file_to_select = request.form.get("filename")
        url_to_change.images_url = file_to_select
        db.session.commit()
        flash(f"เปลี่ยนรูปแสดงสินค้า {url_to_change.product_name} แล้ว")
        return redirect(url_for('dashboard.dashboard1'))

    return render_template("select_image.html", file=files)


@my_dash_board.route("/delete_image/<string:file_delete>", methods=["POST", "GET"])
@login_required
def delete_image(file_delete):
    if os.path.exists(UPLOAD_FOLDER):
        print("ok2")
        file_to_delete = os.path.join(UPLOAD_FOLDER, file_delete)
        os.unlink(file_to_delete)
        print("ok3")
        return redirect(url_for("dashboard.dashboard1"))


@my_dash_board.route('/order_show_up', methods=['GET', 'POST'])
@login_required
def order_show_up():
    order = Order.query.all()
    now = datetime.now()
    if request.method == 'POST':
        order_id = request.form.get("order_id")
        order_to_show = Order.query.filter_by(order_id=order_id).first()
        order_to_show.show_order = False
        db.session.commit()
        return redirect(url_for('dashboard.order_show_up'))

    return render_template("show_order.html", order=order, now=now)




# TODO 3 dashboard decoration
