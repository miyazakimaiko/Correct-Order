import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from functools import wraps
from .forms import UserRegistrationForm, BranchRegistrationForm, ProductRegistrationForm, LoginForm, UpdateAccountForm
from . import app, db, bcrypt, login_manager
from .models import User, Role, Branch, Product, Category
from flask_user import roles_required
from flask_login import login_user, logout_user, current_user
from wtforms.form import BaseForm
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, IntegerField, FormField
import datetime
import calendar


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('userLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


roles = Role.query.all()
branches = Branch.query.all()

b = Category.query.filter_by(name='Breakfast').first()
p = Category.query.filter_by(name='Pastries').first()
l = Category.query.filter_by(name='Lunch').first()
breakfast = Product.query.filter(Product.category.contains(b)).all()
pastry = Product.query.filter(Product.category.contains(p)).all()
lunch = Product.query.filter(Product.category.contains(l)).all()

dates = []

for i in range(7):
    d = datetime.date.today() + datetime.timedelta(days=i)
    date = {'date': d.strftime("%d/%m/%y"),
            'day': d.strftime('%a')}
    dates.append(date)


weeks = []

for i in range(1, 36, 7):
    w = datetime.date.today() + datetime.timedelta(days=i)
    week = w.strftime("%V")
    weeks.append(week)


@app.route("/user-register", methods=['GET', 'POST'])
def userRegister():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        staff_branch = Branch.query.filter_by(name=form.branch.data).first()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,
                    email=form.email.data,
                    branch=[staff_branch,],
                    password=hashed_password)
        staff_role = Role.query.filter_by(name='Staff').first()
        user.roles = [staff_role,]
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}! Now you can login.', 'success')
        return redirect(url_for('userLogin'))
    return render_template('user-register.html', form=form)


@app.route("/branch-register", methods=['GET', 'POST'])
def branchRegister():
    form = BranchRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        branch = User(name=form.name.data,
                      email=form.email.data,
                      password=hashed_password)
        admin_role = Role.query.filter_by(name='Admin').first()
        branch.roles = [admin_role,]
        db.session.add(branch)
        db.session.commit()
        flash(f'Account created for {form.name.data}! Now you can login.', 'success')
        return redirect(url_for('userLogin'))
    return render_template('branch-register.html',
                           form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/user-login", methods=['GET', 'POST'])
def userLogin():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Log in Unsuccessful. Please check email and password', 'danger')
    return render_template('user-login.html',
                           form=form)


@app.route("/user-logout")
def userLogout():
    logout_user()
    return redirect(url_for('userLogin'))


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
    return render_template('account.html',
                           dates=dates,
                           image_file=image_file)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/avatar', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account-edit", methods=['GET', 'POST'])
@login_required
def accountEdit():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        b = Branch.query.filter_by(name=form.branch.data).first()
        current_user.branch = [b,]
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.branch.data = current_user.branch[0].name
    image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
    return render_template('account-edit.html',
                           dates=dates,
                           roles=roles,
                           image_file=image_file,
                           form=form)


@app.route("/products-add", methods=['GET', 'POST'])
@roles_required('Admin')
def productsAdd():
    form = ProductRegistrationForm()
    if form.validate_on_submit():
        c = Category.query.filter_by(name=form.category.data).first()
        if form.acceptable_extra_quantity.data is None:
            product = Product(name=form.name.data,
                              key=form.key.data,
                              category=[c,],
                              oneday_shelf_life=form.oneday_shelf_life.data,
                              acceptable_waste_quantity=form.acceptable_waste_quantity.data,
                              acceptable_extra_quantity=0)
            db.session.add(product)
        elif form.acceptable_waste_quantity.data is None:
            product = Product(name=form.name.data,
                              key=form.key.data,
                              category=[c,],
                              oneday_shelf_life=form.oneday_shelf_life.data,
                              acceptable_waste_quantity=0,
                              acceptable_extra_quantity=form.acceptable_extra_quantity.data)
            db.session.add(product)
        db.session.commit()
        flash(f'Product {form.name.data} is successfully added!', 'success')
        return redirect(url_for('productsAdd'))
    image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
    return render_template('products-add.html',
                           form=form,
                           # items=items,
                           dates=dates,
                           image_file=image_file)


@app.route("/products-edit", methods=['GET', 'POST'])
@roles_required('Admin')
def productEdit():
    def form_form_fields(fields):
        def create_form(prefix='', **kwargs):
            form = BaseForm(fields, prefix=prefix)
            form.process(**kwargs)
            return form
        return create_form

    class UpdateProductForm(FlaskForm):
        products = Product.query.all()
        list_oneday_shelf_life = FormField(form_form_fields([(product.key,
                                                              BooleanField(product))
                                                             for product in products]))
        list_waste_quantity = FormField(form_form_fields([(product.key,
                                                           IntegerField(product))
                                                          for product in products]))
        list_extra_quantity = FormField(form_form_fields([(product.key,
                                                           IntegerField(product))
                                                          for product in products]))
        submit = SubmitField('Update')

    form = UpdateProductForm()
    products = Product.query.all()
    if form.validate_on_submit():
        for p in products:
            p.oneday_shelf_life = form.list_oneday_shelf_life[p.key].data
            p.acceptable_waste_quantity = form.list_waste_quantity[p.key].data
            p.acceptable_extra_quantity = form.list_extra_quantity[p.key].data
        db.session.commit()
        flash(f'Your products has been updated!', 'success')
        return redirect(url_for('productEdit'))
    elif request.method == 'GET':
        for p in products:
            form.list_oneday_shelf_life[p.key].data = p.oneday_shelf_life
            form.list_waste_quantity[p.key].data = p.acceptable_waste_quantity
            form.list_extra_quantity[p.key].data = p.acceptable_extra_quantity

    image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
    products_keys = Product.query.with_entities(Product.key).all()
    return render_template('products-edit.html',
                           products_keys=products_keys,
                           products=products,
                           breakfast=breakfast,
                           pastry=pastry,
                           lunch=lunch,
                           dates=dates,
                           image_file=image_file,
                           form=form)


@app.route("/index")
@login_required
def index():
    image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
    return render_template('index.html',
                           pastry=pastry,
                           breakfast=breakfast,
                           lunch=lunch,
                           dates=dates,
                           weeks=weeks,
                           image_file=image_file)


# @app.route("/day0")
# @login_required
# def day0():
#     image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
#     return render_template('day0.html',
#                            dates=dates,
#                            image_file=image_file)
#
#
# @app.route("/day1")
# @login_required
# def day1():
#     image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
#     return render_template('day1.html',
#                            dates=dates,
#                            image_file=image_file)
#
#
# @app.route("/day2")
# @login_required
# def day2():
#     image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
#     return render_template('day2.html',
#                            dates=dates,
#                            image_file=image_file)
#
#
# @app.route("/day3")
# @login_required
# def day3():
#     image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
#     return render_template('day3.html',
#                            dates=dates,
#                            image_file=image_file)
#
#
# @app.route("/day4")
# @login_required
# def day4():
#     image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
#     return render_template('day4.html',
#                            dates=dates,
#                            image_file=image_file)
#
#
# @app.route("/day5")
# @login_required
# def day5():
#     image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
#     return render_template('day5.html',
#                            dates=dates,
#                            image_file=image_file)
#
#
# @app.route("/day6")
# @login_required
# def day6():
#     image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
#     return render_template('day6.html',
#                            dates=dates,
#                            image_file=image_file)

@app.route("/page-faq")
@login_required
def pageFaq():
    return render_template('page-faq.html')


@app.route("/user-lock-screen")
def userLockScreen():
    return render_template('user-lock-screen.html')


@app.route("/user-forgot-password")
def userForgotPassword():
    return render_template('user-forgot-password.html')


