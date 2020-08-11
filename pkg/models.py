from . import db, app, bcrypt
from flask_user import UserMixin
from flask_user import UserManager

# user_roles = db.Table('user_roles',
#                       db.Column(db.Integer, primary_key=True),
#                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
#                       )

# user_branch = db.Table('user_branch',
#                        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
#                        db.Column('branch_id', db.Integer, db.ForeignKey('branch.id'), primary_key=True)
#                        )


class User(db.Model, UserMixin):
    __tablename__ = 'users'
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
    role_id = db.Column(db.Integer,
                        db.ForeignKey('roles.id'))
    roles = db.relationship("Role",
                            secondary='user_roles')
    branch_id = db.Column(db.Integer,
                          db.ForeignKey('branches.id'))
    branches = db.relationship("Branch",
                               secondary='user_branches')

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.branches}', '{self.image_file}')"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)
    # users = db.relationship('User',
    #                         back_populates="roles",
    #                         lazy=True)

    def __repr__(self):
        return f"Role('{self.id}', '{self.name}')"


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(),
                   primary_key=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(),
                        db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"UserRole('{self.id}', '{self.user_id}', '{self.role_id}')"


class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)

    def __repr__(self):
        return f"Branch('{self.id}', '{self.name}')"


class UserBranch(db.Model):
    __tablename__ = 'user_branches'
    id = db.Column(db.Integer(),
                   primary_key=True)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    branch_id = db.Column(db.Integer(),
                          db.ForeignKey('branches.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"UserBranch('{self.id}', '{self.user_id}', '{self.branch_id}')"


user_manager = UserManager(app, db, User)

product_category = db.Table('categories',
                            db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                            db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
                            )


class Product(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(100),
                     nullable=False)
    key = db.Column(db.String(20),
                    unique=True,
                    nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'))
    category = db.relationship("Category",
                               back_populates="products")

    product_branch = db.relationship('ProductBranch',
                                     backref='ProductBranch.product_id',
                                     primaryjoin='Product.id==ProductBranch.product_id',
                                     lazy='dynamic')

    def __repr__(self):
        return f"Product('{self.id}', '{self.name}', '{self.key}', '{self.category_id}')"


class ProductBranch(db.Model):
    __tablename__ = 'product_branch'
    id = db.Column(db.Integer(),
                   primary_key=True)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('product.id', ondelete='CASCADE'))
    product = db.relationship('Product', foreign_keys='ProductBranch.product_id')
    branch_id = db.Column(db.Integer,
                          db.ForeignKey('branches.id', ondelete='CASCADE'))
    oneday_shelf_life = db.Column(db.Boolean,
                                  default=True)
    acceptable_waste_quantity = db.Column(db.Integer,
                                          default=1)
    acceptable_extra_quantity = db.Column(db.Integer,
                                          default=1)
    prediction_daily = db.Column(db.Integer)
    prediction_weekly = db.Column(db.Integer)
    prediction_monthly = db.Column(db.Integer)

    def __repr__(self):
        return f"ProductBranch(id:{self.id}, product_id:{self.product_id}, branch_id:{self.branch_id}, " \
               f"prediction_daily:{self.prediction_daily}, prediction_weekly:{self.prediction_weekly}, prediction_monthly:{self.prediction_monthly})"


class Category(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)
    products = db.relationship('Product',
                               back_populates="category",
                               lazy=True)

    def __repr__(self):
        return f"Category('{self.id}', '{self.name}', '{self.products}')"


# class ProductCategory(db.Model):
#     __tablename__ = 'product_category'
#     id = db.Column(db.Integer(),
#                    primary_key=True)
#     product_id = db.Column(db.Integer,
#                            db.ForeignKey('product.id', ondelete='CASCADE'))
#     category_id = db.Column(db.Integer,
#                             db.ForeignKey('category.id', ondelete='CASCADE'))


# class PredictionDaily(db.Model):
#     id = db.Column(db.Integer,
#                    primary_key=True)
#     product_branch_id = db.Column(db.Integer,
#                                   db.ForeignKey('product_branch.id'), nullable=False)
#     date = db.Column(db.DateTime,
#                      nullable=False)
#     category = db.Column(db.String,
#                          nullable=False)
#     sales_prediction = db.Column(db.Integer)
#     day_count = db.Column(db.Integer)
#
#     def __repr__(self):
#         return f"PredictionDaily('{self.id}', '{self.date}', '{self.sales_prediction}')"
#
#
# class PredictionWeekly(db.Model):
#     id = db.Column(db.Integer,
#                    primary_key=True)
#     product_branch_id = db.Column(db.Integer,
#                                   db.ForeignKey('product_branch.id'), nullable=False)
#     category = db.Column(db.String,
#                          nullable=False)
#     week = db.Column(db.Integer,
#                      nullable=False)
#     sales_prediction = db.Column(db.Integer)
#     week_count = db.Column(db.Integer)
#
#     def __repr__(self):
#         return f"PredictionWeekly('{self.id}', '{self.week}', '{self.sales_prediction}')"
#
#
# class PredictionMonthly(db.Model):
#     id = db.Column(db.Integer,
#                    primary_key=True)
#     product_branch_id = db.Column(db.Integer,
#                                   db.ForeignKey('product_branch.id'), nullable=False)
#     category = db.Column(db.String,
#                          nullable=False)
#     month = db.Column(db.Integer,
#                       nullable=False)
#     sales_prediction = db.Column(db.Integer)
#     month_count = db.Column(db.Integer)
#
#     def __repr__(self):
#         return f"PredictionMonthly('{self.id}', '{self.month}', '{self.sales_prediction}')"


def init_db():
    db.create_all()

    if Role.query.count() == 0:
        admin_role = Role(name='Admin')
        staff_role = Role(name='Staff')
        db.session.add(admin_role)
        db.session.add(staff_role)
        db.session.commit()

    if Branch.query.count() == 0:
        branch1 = Branch(name='SAS')
        branch2 = Branch(name='PSL')
        branch3 = Branch(name='TCD')
        branch4 = Branch(name='ISFC')
        branch5 = Branch(name='HQ')
        db.session.add(branch1)
        db.session.add(branch2)
        db.session.add(branch3)
        db.session.add(branch4)
        db.session.add(branch5)
        db.session.commit()

    if Category.query.count() == 0:
        category1 = Category(name='Breakfast')
        category2 = Category(name='Lunch')
        category3 = Category(name='Pastries')
        db.session.add(category1)
        db.session.add(category2)
        db.session.add(category3)
        db.session.commit()

    if not User.query.filter(User.email == 'sample@coffeeangel.com').first():
        hashed_password = bcrypt.generate_password_hash('sample').decode('utf-8')
        new_user = User(name='sample', email='sample@coffeeangel.com', password=hashed_password)
        new_user.roles.append(admin_role)
        new_user.branches.append(branch1)
        db.session.add(new_user)
        db.session.commit()

    if Product.query.count() == 0:
        p1 = Product(name='Mixberry Scone', key='BERRY-SCONE', category=category3)
        p2 = Product(name='Plain Croissant', key='PLAIN-CROIS', category=category3)
        p3 = Product(name='Pain Au Raisin', key='PAIN-RAIS', category=category3)
        p4 = Product(name='Pain Au Chocolate', key='PAIN-CHOCO', category=category3)
        p5 = Product(name='Sausage Roll', key='SAUSI-ROLL', category=category1)
        p6 = Product(name='Ham Cheese Croissant', key='HAM-CROIS', category=category1)
        p7 = Product(name='Granola Parfait', key='GRAN-PARF', category=category1)
        p8 = Product(name='Chicken Chutney Wrap', key='CHICK-C-WRAP', category=category2)
        p9 = Product(name='Caprese', key='CAPRESE', category=category2)
        p10 = Product(name='Bacon Brie Bap', key='BAC-BRIE', category=category2)
        p11 = Product(name='Ham Cheese Toastie', key='HAM-TOAST', category=category2)
        p12 = Product(name='Vegan wrap', key='VEG-WRAP', category=category2)
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.add(p5)
        db.session.add(p6)
        db.session.add(p7)
        db.session.add(p8)
        db.session.add(p9)
        db.session.add(p10)
        db.session.add(p11)
        db.session.add(p12)
        db.session.commit()

    if ProductBranch.query.count() == 0:
        branch1 = Branch.query.filter(Branch.name == 'SAS').first()
        scone = Product.query.filter(Product.name == 'Mixberry Scone').first()
        crois = Product.query.filter(Product.name == 'Plain Croissant').first()
        raisin = Product.query.filter(Product.name == 'Pain Au Raisin').first()
        sausi = Product.query.filter(Product.name == 'Sausage Roll').first()
        hamcrois = Product.query.filter(Product.name == 'Ham Cheese Croissant').first()
        parfait = Product.query.filter(Product.name == 'Granola Parfait').first()
        chicken = Product.query.filter(Product.name == 'Chicken Chutney Wrap').first()
        caprese = Product.query.filter(Product.name == 'Caprese').first()
        bacon = Product.query.filter(Product.name == 'Bacon Brie Bap').first()
        toastie = Product.query.filter(Product.name == 'Ham Cheese Toastie').first()
        vegan = Product.query.filter(Product.name == 'Vegan wrap').first()
        choco = Product.query.filter(Product.name == 'Pain Au Chocolate').first()
        pb1 = ProductBranch(product_id=scone.id, branch_id=branch1.id, prediction_daily=10,
                            prediction_weekly=65, prediction_monthly=250)
        pb2 = ProductBranch(product_id=crois.id, branch_id=branch1.id, prediction_daily=8,
                            prediction_weekly=50, prediction_monthly=200)
        pb3 = ProductBranch(product_id=raisin.id, branch_id=branch1.id, prediction_daily=8,
                            prediction_weekly=50, prediction_monthly=200)
        pb4 = ProductBranch(product_id=sausi.id, branch_id=branch1.id, prediction_daily=5,
                            prediction_weekly=30, prediction_monthly=120)
        pb5 = ProductBranch(product_id=hamcrois.id, branch_id=branch1.id, prediction_daily=5,
                            prediction_weekly=30, prediction_monthly=120)
        pb6 = ProductBranch(product_id=parfait.id, branch_id=branch1.id, prediction_daily=3,
                            prediction_weekly=20, prediction_monthly=80)
        pb7 = ProductBranch(product_id=chicken.id, branch_id=branch1.id, prediction_daily=4,
                            prediction_weekly=24, prediction_monthly=90)
        pb8 = ProductBranch(product_id=caprese.id, branch_id=branch1.id, prediction_daily=2,
                            prediction_weekly=12, prediction_monthly=50)
        pb9 = ProductBranch(product_id=bacon.id, branch_id=branch1.id, prediction_daily=4,
                            prediction_weekly=24, prediction_monthly=90)
        pb10 = ProductBranch(product_id=toastie.id, branch_id=branch1.id, prediction_daily=3,
                             prediction_weekly=18, prediction_monthly=55)
        pb11 = ProductBranch(product_id=vegan.id, branch_id=branch1.id, prediction_daily=2,
                             prediction_weekly=12, prediction_monthly=50)
        pb12 = ProductBranch(product_id=choco.id, branch_id=branch1.id, prediction_daily=8,
                             prediction_weekly=50, prediction_monthly=200)
        db.session.add(pb1)
        db.session.add(pb2)
        db.session.add(pb3)
        db.session.add(pb4)
        db.session.add(pb5)
        db.session.add(pb6)
        db.session.add(pb7)
        db.session.add(pb8)
        db.session.add(pb9)
        db.session.add(pb10)
        db.session.add(pb11)
        db.session.add(pb12)
        db.session.commit()


init_db()
