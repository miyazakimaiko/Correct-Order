from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User, Branch, Category, Product
from flask_login import current_user


class UserRegistrationForm(FlaskForm):
    name = StringField('Username',
                       validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    branch = SelectField('Branch',
                         choices=[(branch.name, branch.name)
                                  for branch in Branch.query.all()])

    password = PasswordField('Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('That name is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class BranchRegistrationForm(FlaskForm):
    name = StringField('Branch name',
                       validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()

        if user:
            raise ValidationError('That name is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    name = StringField('Username',
                       validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    branch = SelectField('Branch',
                         choices=[(branch.name, branch.name)
                                  for branch in Branch.query.all()])

    picture = FileField('Change Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('That name is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class ProductRegistrationForm(FlaskForm):
    name = StringField('Product Name',
                       validators=[DataRequired(), Length(min=2, max=20)])

    key = StringField('Product Key',
                      validators=[DataRequired(), Length(min=2, max=20)])

    category = SelectField('Category',
                           choices=[(category.name, category.name)
                                    for category in Category.query.all()])

    oneday_shelf_life = BooleanField()

    acceptable_waste_quantity = IntegerField('Acceptable Waste Quantity')

    acceptable_extra_quantity = IntegerField('Acceptable Extra Quantity')

    submit = SubmitField('Submit Product')

    def validate_name(self, name):
        product = Product.query.filter_by(name=name.data).first()
        if product:
            raise ValidationError('That name is taken. Please choose a different one.')

    def validate_key(self, key):
        product = Product.query.filter_by(key=key.data).first()
        if product:
            raise ValidationError('That keyword is taken. Please choose a different one.')