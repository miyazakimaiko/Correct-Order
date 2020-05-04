from . import db, app, bcrypt
from flask_user import UserMixin
from flask_user import UserManager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(20),
                     unique=True,
                     nullable=False)
    email = db.Column(db.String(120),
                      unique=True,
                      nullable=False)
    image_file = db.Column(db.String(20),
                           nullable=False,
                           default='default.png')
    password = db.Column(db.String(60),
                         nullable=False)
    branch = db.relationship('Branch',
                             secondary='user_branches')
    roles = db.relationship('Role',
                            secondary='user_roles')
    prediction_daily = db.relationship('PredictionDaily',
                                       backref='location',
                                       lazy=True)
    prediction_weekly = db.relationship('PredictionWeekly',
                                        backref='location',
                                        lazy=True)
    prediction_monthly = db.relationship('PredictionMonthly',
                                         backref='location',
                                         lazy=True)

    def __repr__(self):
        return f"User('{self. name}', '{self.email}', '{self.image_file}')"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(),
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(),
                   primary_key=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(),
                        db.ForeignKey('roles.id', ondelete='CASCADE'))


class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer(),
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)
    user_id = db.column(db.Integer,
                        db.ForeignKey('user.id'))


class UserBranch(db.Model):
    __tablename__ = 'user_branches'
    id = db.Column(db.Integer(),
                   primary_key=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id', ondelete='CASCADE'))
    branch_id = db.Column(db.Integer(),
                          db.ForeignKey('branches.id', ondelete='CASCADE'))


user_manager = UserManager(app, db, User)


class Product(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(100),
                     nullable=False)
    key = db.Column(db.String(20),
                    unique=True,
                    nullable=False)
    category = db.relationship('Category',
                               secondary='product_categories')
    oneday_shelf_life = db.Column(db.Boolean,
                                  default=True)
    acceptable_waste_quantity = db.Column(db.Integer(),
                                          default=0)
    acceptable_extra_quantity = db.Column(db.Integer(),
                                          default=0)
    prediction_daily = db.relationship('PredictionDaily',
                                       backref='item',
                                       lazy=True)
    prediction_weekly = db.relationship('PredictionWeekly',
                                        backref='item',
                                        lazy=True)
    prediction_monthly = db.relationship('PredictionMonthly',
                                         backref='item',
                                         lazy=True)

    def __repr__(self):
        return f"Product('{self.name}', '{self.key}', '{self.category}', '{self.oneday_shelf_life}'," \
               f"'{self.acceptable_extra_quantity}','{self.acceptable_waste_quantity}')"


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(),
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)
    product_id = db.column(db.Integer,
                           db.ForeignKey('product.id'))


class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer(),
                   primary_key=True)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('product.id', ondelete='CASCADE'))
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.id', ondelete='CASCADE'))


class PredictionDaily(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    branch_id = db.Column(db.Integer,
                          db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('product.id'), nullable=False)
    date = db.Column(db.DateTime,
                     nullable=False)
    category = db.Column(db.String,
                         nullable=False)
    sales_prediction = db.Column(db.Integer)
    day_count = db.Column(db.Integer)

    def __repr__(self):
        return f"PredictionDaily('{self.id}', '{self.date}', '{self.sales_prediction}')"


class PredictionWeekly(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    branch_id = db.Column(db.Integer,
                          db.ForeignKey('user.id'),
                          nullable=False)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('product.id'),
                           nullable=False)
    category = db.Column(db.String,
                         nullable=False)
    week = db.Column(db.Integer,
                     nullable=False)
    sales_prediction = db.Column(db.Integer)
    week_count = db.Column(db.Integer)

    def __repr__(self):
        return f"PredictionWeekly('{self.id}', '{self.week}', '{self.sales_prediction}')"


class PredictionMonthly(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    branch_id = db.Column(db.Integer,
                          db.ForeignKey('user.id'),
                          nullable=False)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('product.id'),
                           nullable=False)
    category = db.Column(db.String,
                         nullable=False)
    month = db.Column(db.Integer,
                      nullable=False)
    sales_prediction = db.Column(db.Integer)
    month_count = db.Column(db.Integer)

    def __repr__(self):
        return f"PredictionMonthly('{self.id}', '{self.month}', '{self.sales_prediction}')"


def init_db():
    db.create_all()
    admin_role = Role(name='Admin')
    branch1 = Branch(name='SAS')
    category1 = Category(name='Breakfast')
    db.session.commit()

    hashed_password = bcrypt.generate_password_hash('sample').decode('utf-8')
    new_user = User(name='sample', email='sample@coffeeangel.com', password=hashed_password)
    new_user.Role = [admin_role,]
    new_user.branches = [branch1,]
    db.session.commit()


init_db()