from . import db, app, bcrypt
from flask_user import UserMixin
from flask_user import UserManager


user_role = db.Table('roles',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                     )


user_branch = db.Table('branches',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('branch_id', db.Integer, db.ForeignKey('branch.id'), primary_key=True)
                       )


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
        return f"User('{self. name}', '{self.email}', '{self.branch}', '{self.image_file}')"


class Role(db.Model):
    id = db.Column(db.Integer(),
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)
    users = db.relationship('User',
                            lazy=True)


# class UserRole(db.Model):
#     __tablename__ = 'user_role'
#     id = db.Column(db.Integer(),
#                    primary_key=True)
#     user_id = db.Column(db.Integer(),
#                         db.ForeignKey('user.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(),
#                         db.ForeignKey('roles.id', ondelete='CASCADE'))


class Branch(db.Model):
    id = db.Column(db.Integer(),
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)
    users = db.relationship('User',
                            lazy=True)



# class UserBranch(db.Model):
#     __tablename__ = 'user_branch'
#     id = db.Column(db.Integer(),
#                    primary_key=True)
#     user_id = db.Column(db.Integer(),
#                         db.ForeignKey('user.id', ondelete='CASCADE'))
#     branch_id = db.Column(db.Integer(),
#                           db.ForeignKey('branches.id', ondelete='CASCADE'))


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
    # branch = db.relationship('Branch',
    #                          secondary='product_branch')
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


# class ProductBranch(db.Model):
#     __tablename__ = 'product_branch'
#     id = db.Column(db.Integer(),
#                    primary_key=True)
#     product_id = db.Column(db.Integer,
#                            db.ForeignKey('product.id', ondelete='CASCADE'))
#     branch_id = db.Column(db.Integer,
#                           db.ForeignKey('branches.id', ondelete='CASCADE'))


class Category(db.Model):
    id = db.Column(db.Integer(),
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)
    products = db.relationship('Product',
                               lazy=True)



# class ProductCategory(db.Model):
#     __tablename__ = 'product_category'
#     id = db.Column(db.Integer(),
#                    primary_key=True)
#     product_id = db.Column(db.Integer,
#                            db.ForeignKey('product.id', ondelete='CASCADE'))
#     category_id = db.Column(db.Integer,
#                             db.ForeignKey('categories.id', ondelete='CASCADE'))


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
    staff_role = Role(name='Staff')
    branch1 = Branch(name='SAS')
    branch2 = Branch(name='PSL')
    branch3 = Branch(name='TCD')
    branch4 = Branch(name='ISFC')
    branch5 = Branch(name='HQ')
    category1 = Category(name='Breakfast')
    category2 = Category(name='Lunch')
    category3 = Category(name='Pastries')
    db.session.add(admin_role)
    db.session.add(staff_role)
    db.session.add(branch1)
    db.session.add(branch2)
    db.session.add(branch3)
    db.session.add(branch4)
    db.session.add(branch5)
    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.commit()

    hashed_password = bcrypt.generate_password_hash('sample').decode('utf-8')
    new_user = User(name='sample', email='sample@coffeeangel.com', password=hashed_password)
    new_user.role = [admin_role,]
    new_user.branch = [branch1,]

    new_product = Product(name='sample', key='SAMPLE')
    new_product.category = [category1,]
    new_product.branch = [branch1,]

    db.session.add(new_user)
    db.session.add(new_product)
    db.session.commit()


init_db()