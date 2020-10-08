from flask import render_template, url_for, flash, redirect, request, session
from functools import wraps
from .forms import UserRegistrationForm, BranchRegistrationForm, LoginForm, UpdateAccountForm
from . import app, db, bcrypt, login_manager
from .models import User, Role, Branch, Category, ProductSAS, ProductHQ, ProductISFC, ProductPSL, ProductTCD
from .talech_keys import grant_type, client_id_1, client_id_2, client_secret_1, client_secret_2, \
    client_version, token_url, refresh_token_1, refresh_token_2, ID_HQ, ID_IFSC, ID_PSL, ID_SAS, ID_TCD
from flask_user import roles_required
from flask_login import login_user, logout_user, current_user
from wtforms.form import BaseForm
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, IntegerField, FormField
import datetime
from flask.json import jsonify
import json
import requests
import time
import pprint
import pandas as pd


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

dates = []

for i in range(8):
    d = datetime.date.today() + datetime.timedelta(days=i)
    date = {'date': d.strftime("%d/%m/%y"),
            'day': d.strftime('%a')}
    dates.append(date)


from .functions import get_recent_week_nums


weeks = get_recent_week_nums()


@app.route("/user-register", methods=['GET', 'POST'])
def user_register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        staff_branch = Branch.query.filter_by(name=form.branch.data).first()
        staff_role = Role.query.filter_by(name='Staff').first()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,
                    email=form.email.data,
                    branches=staff_branch,
                    role=staff_role,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}! Now you can login.', 'success')
        return redirect(url_for('user_login'))
    return render_template('user-register.html', form=form)


@app.route("/branch-register", methods=['GET', 'POST'])
def branch_register():
    form = BranchRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin_branch = Branch.query.filter_by(name=form.branch.data).first()
        admin_role = Role.query.filter_by(name='Admin').first()
        branch = User(name=form.name.data,
                      email=form.email.data,
                      password=hashed_password,
                      branches=admin_branch,
                      role=admin_role
                      )
        db.session.add(branch)
        db.session.commit()
        flash(f'Account created for {form.name.data}! Now you can login.', 'success')
        return redirect(url_for('user_login'))
    return render_template('branch-register.html',
                           form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/user-login", methods=['GET', 'POST'])
def user_login():
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
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
    return render_template('account.html',
                           dates=dates,
                           image_file=image_file)


from .functions import save_picture


@app.route("/account-edit", methods=['GET', 'POST'])
@login_required
def account_edit():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        b = Branch.query.filter_by(name=form.branch.data).first()
        current_user.branches = [b,]
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.branch.data = current_user.branches[0].name
    image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
    return render_template('account-edit.html',
                           dates=dates,
                           roles=roles,
                           image_file=image_file,
                           form=form)


# @app.route("/products-add", methods=['GET', 'POST'])
# @roles_required('Admin')
# def productsAdd():
#     form = ProductRegistrationForm()
#     if form.validate_on_submit():
#         c = Category.query.filter_by(name=form.category.data).first()
#         if form.acceptable_extra_quantity.data is None:
#             product = Product(name=form.name.data,
#                               key=form.key.data,
#                               category=c,
#                               oneday_shelf_life=form.oneday_shelf_life.data,
#                               acceptable_waste_quantity=form.acceptable_waste_quantity.data,
#                               acceptable_extra_quantity=0)
#             db.session.add(product)
#         elif form.acceptable_waste_quantity.data is None:
#             product = Product(name=form.name.data,
#                               key=form.key.data,
#                               category=c,
#                               oneday_shelf_life=form.oneday_shelf_life.data,
#                               acceptable_waste_quantity=0,
#                               acceptable_extra_quantity=form.acceptable_extra_quantity.data)
#             db.session.add(product)
#         db.session.commit()
#         flash(f'Product {form.name.data} is successfully added!', 'success')
#         return redirect(url_for('productsAdd'))
#     image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
#     return render_template('products-add.html',
#                            form=form,
#                            # items=items,
#                            dates=dates,
#                            image_file=image_file)


@app.route("/products-edit", methods=['GET', 'POST'])
@roles_required('Admin')
def product_edit():
    def form_form_fields(fields):
        def create_form(prefix='', **kwargs):
            form = BaseForm(fields, prefix=prefix)
            form.process(**kwargs)
            return form
        return create_form

    if current_user.is_authenticated:
        current_branch_name = current_user.branches[0].name
        if current_branch_name == 'SAS':
            product = ProductSAS
        if current_branch_name == 'HQ':
            product = ProductHQ
        if current_branch_name == 'PSL':
            product = ProductPSL
        if current_branch_name == 'TCD':
            product = ProductTCD
        if current_branch_name == 'ISFC':
            product = ProductISFC
    products = product.query.all()

    class UpdateProductForm(FlaskForm):
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

    b = Category.query.filter_by(name='Breakfast').first()
    p = Category.query.filter_by(name='Pastries').first()
    l = Category.query.filter_by(name='Lunch').first()
    breakfast = product.query.filter_by(category=b).all()
    pastry = product.query.filter_by(category=p).all()
    lunch = product.query.filter_by(category=l).all()

    image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
    products_keys = product.query.with_entities(product.key).all()
    return render_template('products-edit.html',
                           products_keys=products_keys,
                           products=products,
                           breakfast=breakfast,
                           pastry=pastry,
                           lunch=lunch,
                           dates=dates,
                           image_file=image_file,
                           form=form)


@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    if current_user.is_authenticated:
        data = {
            'grant_type': grant_type,
            'client_id': client_id_1,
            'client_secret': client_secret_1,
            'refresh_token': refresh_token_1,
            'client_version': client_version
        }
        resp = requests.post(url=token_url,
                             json=data)
        resp_json = resp.json()
        session['oauth_token'] = resp_json['access_token']
        return redirect(url_for('.profile'))
        # return jsonify(resp.json())
    #     current_branch_name = current_user.branches[0].name
    #     if current_branch_name == 'SAS':
    #         product = ProductSAS
    #     if current_branch_name == 'HQ':
    #         product = ProductHQ
    #     if current_branch_name == 'PSL':
    #         product = ProductPSL
    #     if current_branch_name == 'TCD':
    #         product = ProductTCD
    #     if current_branch_name == 'ISFC':
    #         product = ProductISFC
    # b = Category.query.filter_by(name='Breakfast').first()
    # p = Category.query.filter_by(name='Pastries').first()
    # l = Category.query.filter_by(name='Lunch').first()
    # breakfast = product.query.filter_by(category_id=b.id).all()
    # pastry = product.query.filter_by(category_id=p.id).all()
    # lunch = product.query.filter_by(category_id=l.id).all()
    # image_file = url_for('static', filename='images/avatar/' + current_user.image_file)
    # return render_template('index.html',
    #                        branch_name=current_branch_name,
    #                        pastry=pastry,
    #                        breakfast=breakfast,
    #                        lunch=lunch,
    #                        dates=dates,
    #                        weeks=weeks,
    #                        image_file=image_file)


from .functions import json_get_sales_count, json_get_fooditem_keys, \
    merge_data, get_dynamic_dates_from, modify_into_training_data


@app.route("/profile", methods=["GET", "POST"])
def profile():
    def get_summary_report(token, startdate, enddate):
        arr = {
            'searchCriteria': {
                'startDate': startdate,
                'endDate': enddate,
                'includedReports': [102]
            }
        }
        result = requests.post(url='https://mapi-eu.talech.com/reports/receiptssummaryreport',
                               json=arr,
                               headers=token)
        items = result.json()
        salesdata = json_get_sales_count(items)
        return salesdata

    days = get_dynamic_dates_from(-30, -2)
    token = {
        'securityToken': session['oauth_token'],
        'X-POS-MerchantId': ID_SAS
    }

    dailysales = {}
    for i in range(1, len(days)):
        salesdata = get_summary_report(token, days[i-1], days[i])
        dailysales[days[i-1]] = salesdata

    itemsearchdata = {
        'searchCriteria': {
            'offset': 0,
            'inventoryOnly': False
        }
    }
    url = 'https://mapi-eu.talech.com/managemenu/menuitem/allmenuitems'
    menuresult = requests.post(url=url,
                               json=itemsearchdata,
                               headers=token)
    items = menuresult.json()
    itemkeys = json_get_fooditem_keys(items)
    merged = merge_data(dailysales, itemkeys)
    modify = modify_into_training_data(merged)

    return jsonify(modify)
    # return redirect(url_for('.profile', salesdata=merged))


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


