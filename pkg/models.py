from . import db, app, bcrypt
from flask_user import UserMixin
from flask_user import UserManager
from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin, OAuth2TokenMixin
from datetime import datetime, timedelta


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

    def get_user_id(self):
        return self.id

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.branches}', '{self.image_file}')"


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)

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

product_sas_category = db.Table('categories_sas',
                                db.Column('product_sas_id',
                                          db.Integer,
                                          db.ForeignKey('product_sas.id'),
                                          primary_key=True),
                                db.Column('category_id',
                                          db.Integer,
                                          db.ForeignKey('category.id'),
                                          primary_key=True)
                                )
product_hq_category = db.Table('categories_hq',
                               db.Column('product_hq_id',
                                         db.Integer,
                                         db.ForeignKey('product_hq.id'),
                                         primary_key=True),
                               db.Column('category_id',
                                         db.Integer,
                                         db.ForeignKey('category.id'),
                                         primary_key=True)
                               )
product_psl_category = db.Table('categories_psl',
                                db.Column('product_psl_id',
                                          db.Integer,
                                          db.ForeignKey('product_psl.id'),
                                          primary_key=True),
                                db.Column('category_id',
                                          db.Integer,
                                          db.ForeignKey('category.id'),
                                          primary_key=True)
                                )
product_tcd_category = db.Table('categories_tcd',
                                db.Column('product_tcd_id',
                                          db.Integer,
                                          db.ForeignKey('product_tcd.id'),
                                          primary_key=True),
                                db.Column('category_id',
                                          db.Integer,
                                          db.ForeignKey('category.id'),
                                          primary_key=True)
                                )
product_isfc_category = db.Table('categories_isfc',
                                 db.Column('product_isfc_id',
                                           db.Integer,
                                           db.ForeignKey('product_isfc.id'),
                                           primary_key=True),
                                 db.Column('category_id',
                                           db.Integer,
                                           db.ForeignKey('category.id'),
                                           primary_key=True)
                                 )

prediction_daily_sas = db.Table('prediction_daily_sas',
                                db.Column('product_id',
                                          db.Integer,
                                          db.ForeignKey('product_sas.id'),
                                          primary_key=True),
                                db.Column('prediction_id',
                                          db.Integer,
                                          db.ForeignKey('prediction_daily.id'),
                                          primary_key=True)
                                )

prediction_weekly_sas = db.Table('prediction_weekly_sas',
                                 db.Column('product_id',
                                           db.Integer,
                                           db.ForeignKey('product_sas.id'),
                                           primary_key=True),
                                 db.Column('prediction_id',
                                           db.Integer,
                                           db.ForeignKey('prediction_weekly.id'),
                                           primary_key=True)
                                 )


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(100),
                     nullable=False)
    key = db.Column(db.String(20),
                    unique=True,
                    nullable=False)
    oneday_shelf_life = db.Column(db.Boolean,
                                  default=True)
    acceptable_waste_quantity = db.Column(db.Integer,
                                          default=1)
    acceptable_extra_quantity = db.Column(db.Integer,
                                          default=1)

    def __repr__(self):
        return f"Product(id:{self.id}, name:{self.name}," \
               f" key:{self.key}, category_id:{self.category_id}, " \
               f"prediction_daily:{self.prediction_daily}, " \
               f"prediction_weekly:{self.prediction_daily})"


class ProductSAS(Product):
    __tablename__ = 'product_sas'
    id = db.Column(db.Integer,
                   db.ForeignKey('product.id'),
                   primary_key=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'))
    category = db.relationship("Category",
                               back_populates="products_sas")
    prediction_daily_id = db.Column(db.Integer,
                                    db.ForeignKey('prediction_daily.id'))
    prediction_daily = db.relationship("PredictionDaily",
                                       back_populates="products_sas")
    prediction_weekly_id = db.Column(db.Integer,
                                     db.ForeignKey('prediction_weekly.id'))
    prediction_weekly = db.relationship("PredictionWeekly",
                                        back_populates="products_sas")


class ProductHQ(Product):
    __tablename__ = 'product_hq'
    id = db.Column(db.Integer,
                   db.ForeignKey('product.id'),
                   primary_key=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'))
    category = db.relationship("Category",
                               back_populates="products_hq")
    prediction_daily_id = db.Column(db.Integer,
                                    db.ForeignKey('prediction_daily.id'))
    prediction_daily = db.relationship("PredictionDaily",
                                       back_populates="products_hq")
    prediction_weekly_id = db.Column(db.Integer,
                                     db.ForeignKey('prediction_weekly.id'))
    prediction_weekly = db.relationship("PredictionWeekly",
                                        back_populates="products_hq")


class ProductPSL(Product):
    __tablename__ = 'product_psl'
    id = db.Column(db.Integer,
                   db.ForeignKey('product.id'),
                   primary_key=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'))
    category = db.relationship("Category",
                               back_populates="products_psl")
    prediction_daily_id = db.Column(db.Integer,
                                    db.ForeignKey('prediction_daily.id'))
    prediction_daily = db.relationship("PredictionDaily",
                                       back_populates="products_psl")
    prediction_weekly_id = db.Column(db.Integer,
                                     db.ForeignKey('prediction_weekly.id'))
    prediction_weekly = db.relationship("PredictionWeekly",
                                        back_populates="products_psl")


class ProductTCD(Product):
    __tablename__ = 'product_tcd'
    id = db.Column(db.Integer,
                   db.ForeignKey('product.id'),
                   primary_key=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'))
    category = db.relationship("Category",
                               back_populates="products_tcd")
    prediction_daily_id = db.Column(db.Integer,
                                    db.ForeignKey('prediction_daily.id'))
    prediction_daily = db.relationship("PredictionDaily",
                                       back_populates="products_tcd")
    prediction_weekly_id = db.Column(db.Integer,
                                     db.ForeignKey('prediction_weekly.id'))
    prediction_weekly = db.relationship("PredictionWeekly",
                                        back_populates="products_tcd")


class ProductISFC(Product):
    __tablename__ = 'product_isfc'
    id = db.Column(db.Integer,
                   db.ForeignKey('product.id'),
                   primary_key=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'))
    category = db.relationship("Category",
                               back_populates="products_isfc")
    prediction_daily_id = db.Column(db.Integer,
                                    db.ForeignKey('prediction_daily.id'))
    prediction_daily = db.relationship("PredictionDaily",
                                       back_populates="products_isfc")
    prediction_weekly_id = db.Column(db.Integer,
                                     db.ForeignKey('prediction_weekly.id'))
    prediction_weekly = db.relationship("PredictionWeekly",
                                        back_populates="products_isfc")


class PredictionDaily(db.Model):
    __tablename__ = 'prediction_daily'
    id = db.Column(db.Integer,
                   primary_key=True)
    branch_id = db.Column(db.Integer,
                          nullable=False)
    product_id = db.Column(db.Integer,
                           nullable=False)
    day1 = db.Column(db.Integer,
                     default=0)
    day2 = db.Column(db.Integer,
                     default=0)
    day3 = db.Column(db.Integer,
                     default=0)
    day4 = db.Column(db.Integer,
                     default=0)
    day5 = db.Column(db.Integer,
                     default=0)
    day6 = db.Column(db.Integer,
                     default=0)
    day7 = db.Column(db.Integer,
                     default=0)
    products_sas = db.relationship('ProductSAS',
                                   back_populates="prediction_daily",
                                   lazy=True)
    products_hq = db.relationship('ProductHQ',
                                  back_populates="prediction_daily",
                                  lazy=True)
    products_psl = db.relationship('ProductPSL',
                                   back_populates="prediction_daily",
                                   lazy=True)
    products_tcd = db.relationship('ProductTCD',
                                   back_populates="prediction_daily",
                                   lazy=True)
    products_isfc = db.relationship('ProductISFC',
                                    back_populates="prediction_daily",
                                    lazy=True)

    def __repr__(self):
        return f"PredictionDaily(day1:{self.day1}, " \
               f"day2:{self.day2}, day3:{self.day3}, day4:{self.day4}, " \
               f"day5:{self.day5}, day6:{self.day6}, day7:{self.day7})"


class PredictionWeekly(db.Model):
    __tablename__ = 'prediction_weekly'
    id = db.Column(db.Integer,
                   primary_key=True)
    branch_id = db.Column(db.Integer,
                          nullable=False)
    product_id = db.Column(db.Integer,
                           nullable=False)
    week0 = db.Column(db.Integer,
                      default=0)
    week1 = db.Column(db.Integer,
                      default=0)
    week2 = db.Column(db.Integer,
                      default=0)
    week3 = db.Column(db.Integer,
                      default=0)
    week4 = db.Column(db.Integer,
                      default=0)
    products_sas = db.relationship('ProductSAS',
                                   back_populates="prediction_weekly",
                                   lazy=True)
    products_hq = db.relationship('ProductHQ',
                                  back_populates="prediction_weekly",
                                  lazy=True)
    products_psl = db.relationship('ProductPSL',
                                   back_populates="prediction_weekly",
                                   lazy=True)
    products_tcd = db.relationship('ProductTCD',
                                   back_populates="prediction_weekly",
                                   lazy=True)
    products_isfc = db.relationship('ProductISFC',
                                    back_populates="prediction_weekly",
                                    lazy=True)

    def __repr__(self):
        return f"PredictionWeekly(week0:{self.week0}, " \
               f"week1:{self.week1}, week2:{self.week2}, week3:{self.week3}, " \
               f"week4:{self.week4})"


class Category(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(50),
                     unique=True)
    products_sas = db.relationship('ProductSAS',
                                   back_populates="category",
                                   lazy=True)
    products_hq = db.relationship('ProductHQ',
                                  back_populates="category",
                                  lazy=True)
    products_psl = db.relationship('ProductPSL',
                                   back_populates="category",
                                   lazy=True)
    products_tcd = db.relationship('ProductTCD',
                                   back_populates="category",
                                   lazy=True)
    products_isfc = db.relationship('ProductISFC',
                                    back_populates="category",
                                    lazy=True)

    def __repr__(self):
        return f"Category('{self.id}', '{self.name}')"


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

    if not User.query.filter(User.email == 'sas@coffeeangel.com').first():
        hashed_password = bcrypt.generate_password_hash('sample').decode('utf-8')
        new_user = User(name='sas admin',
                        email='sas@coffeeangel.com',
                        password=hashed_password)
        new_user.roles.append(admin_role)
        new_user.branches.append(branch1)
        db.session.add(new_user)
        db.session.commit()

    if not User.query.filter(User.email == 'hq@coffeeangel.com').first():
        hashed_password = bcrypt.generate_password_hash('sample').decode('utf-8')
        new_user = User(name='hq admin',
                        email='hq@coffeeangel.com',
                        password=hashed_password)
        new_user.roles.append(admin_role)
        new_user.branches.append(branch5)
        db.session.add(new_user)
        db.session.commit()

    if not User.query.filter(User.email == 'tcd@coffeeangel.com').first():
        hashed_password = bcrypt.generate_password_hash('sample').decode('utf-8')
        new_user = User(name='tcd admin',
                        email='tcd@coffeeangel.com',
                        password=hashed_password)
        new_user.roles.append(admin_role)
        new_user.branches.append(branch3)
        db.session.add(new_user)
        db.session.commit()

    if not User.query.filter(User.email == 'psl@coffeeangel.com').first():
        hashed_password = bcrypt.generate_password_hash('sample').decode('utf-8')
        new_user = User(name='psl admin',
                        email='psl@coffeeangel.com',
                        password=hashed_password)
        new_user.roles.append(admin_role)
        new_user.branches.append(branch2)
        db.session.add(new_user)
        db.session.commit()

    if not User.query.filter(User.email == 'isfc@coffeeangel.com').first():
        hashed_password = bcrypt.generate_password_hash('sample').decode('utf-8')
        new_user = User(name='isfc admin',
                        email='isfc@coffeeangel.com',
                        password=hashed_password)
        new_user.roles.append(admin_role)
        new_user.branches.append(branch4)
        db.session.add(new_user)
        db.session.commit()

    if ProductSAS.query.count() == 0:
        branch_sas = Branch.query.filter_by(name='SAS').first()
        p1 = ProductSAS(name='Mixberry Scone',
                        key='BERRY-SCONE',
                        category=category3)
        p2 = ProductSAS(name='Plain Croissant',
                        key='PLAIN-CROIS',
                        category=category3)
        p3 = ProductSAS(name='Pain Au Raisin',
                        key='PAIN-RAIS',
                        category=category3)
        p4 = ProductSAS(name='Pain Au Chocolate',
                        key='PAIN-CHOCO',
                        category=category3)
        p5 = ProductSAS(name='Sausage Roll',
                        key='SAUSI-ROLL',
                        category=category1)
        p6 = ProductSAS(name='Ham Cheese Croissant',
                        key='HAM-CROIS',
                        category=category1)
        p7 = ProductSAS(name='Granola Parfait',
                        key='GRAN-PARF',
                        category=category1)
        p8 = ProductSAS(name='Chicken Chutney Wrap',
                        key='CHICK-C-WRAP',
                        category=category2)
        p9 = ProductSAS(name='Caprese',
                        key='CAPRESE',
                        category=category2)
        p10 = ProductSAS(name='Bacon Brie Bap',
                         key='BAC-BRIE',
                         category=category2)
        p11 = ProductSAS(name='Ham Cheese Toastie',
                         key='HAM-TOAST',
                         category=category2)
        p12 = ProductSAS(name='Vegan wrap',
                         key='VEG-WRAP',
                         category=category2)
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
        pd1 = PredictionDaily(branch_id=branch_sas.id, product_id=p1.id)
        pd2 = PredictionDaily(branch_id=branch_sas.id, product_id=p2.id)
        pd3 = PredictionDaily(branch_id=branch_sas.id, product_id=p3.id)
        pd4 = PredictionDaily(branch_id=branch_sas.id, product_id=p4.id)
        pd5 = PredictionDaily(branch_id=branch_sas.id, product_id=p5.id)
        pd6 = PredictionDaily(branch_id=branch_sas.id, product_id=p6.id)
        pd7 = PredictionDaily(branch_id=branch_sas.id, product_id=p7.id)
        pd8 = PredictionDaily(branch_id=branch_sas.id, product_id=p8.id)
        pd9 = PredictionDaily(branch_id=branch_sas.id, product_id=p9.id)
        pd10 = PredictionDaily(branch_id=branch_sas.id, product_id=p10.id)
        pd11 = PredictionDaily(branch_id=branch_sas.id, product_id=p11.id)
        pd12 = PredictionDaily(branch_id=branch_sas.id, product_id=p12.id)
        p1.prediction_daily = pd1
        p2.prediction_daily = pd2
        p3.prediction_daily = pd3
        p4.prediction_daily = pd4
        p5.prediction_daily = pd5
        p6.prediction_daily = pd6
        p7.prediction_daily = pd7
        p8.prediction_daily = pd8
        p9.prediction_daily = pd9
        p10.prediction_daily = pd10
        p11.prediction_daily = pd11
        p12.prediction_daily = pd12
        db.session.commit()

    # if Client.query.count() == 0:
    #     u1 = User.query.filter_by(name='sas admin').first()
    #     client1 = Client(
    #         user_id=u1.id,
    #         client_id='myzkmik19922@gmail.com',
    #         is_confidential=True,
    #         client_secret='7Ac7YPNgcsgzxhiE',
    #         _redirect_uris=(
    #             'http://localhost:8000/authorized '
    #             'http://localhost/authorized'
    #         ),
    #     )
    #     db.session.add(client1)
    #     db.session.commit()
    #
    # if Grant.query.count() == 0:
    #     temp_grant = Grant(
    #         user_id=1,
    #         client_id='myzkmik19922@gmail.com',
    #         code='12345',
    #         expires=datetime.utcnow() + timedelta(seconds=100)
    #     )
    #     db.session.add(temp_grant)
    #     db.session.commit()
    #
    # if Token.query.count() == 0:
    #     access_token = Token(
    #         user_id=1, client_id='myzkmik19922@gmail.com',
    #         refresh_token='36446748/QX35Y7TCypuuZtgcAvWPAbUN'
    #     )
    #     db.session.add(access_token)
    #     db.session.commit()


init_db()
