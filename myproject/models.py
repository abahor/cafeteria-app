from datetime import datetime

from flask import abort, flash
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash

from myproject import db, login


# from myproject import app


# from myproject import wa


# from myproject import ma


@login.user_loader
def load_user(user_id):
    return UsersModel.query.get(user_id)


class UsersModel(db.Model, UserMixin):
    __tablename__ = 'UsersModel'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    employee_id = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    mobile = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    profile_pic = db.Column(db.String(64), nullable=False)

    orders = db.relationship('Orders', backref='author', lazy='dynamic')

    def __init__(self, email, employee_id, mobile, username, password, path):
        self.username = username
        self.email = email
        self.employee_id = employee_id
        self.mobile = mobile
        self.profile_pic = path
        self.password = generate_password_hash(password)

    def check_password(self, field):
        return check_password_hash(self.password, field)


class MenuList(db.Model):
    __tablename__ = "MenuList"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False, )
    preparation_time = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False, )
    description = db.Column(db.Text, nullable=False, )
    type = db.Column(db.String(64), nullable=False, )
    content = db.relationship('Orders', backref='meal', lazy='dynamic')

    def __init__(self, title, description, type, price, preparation_time):
        self.type = type
        self.title = title
        self.price = price
        self.description = description
        self.preparation_time = preparation_time


class Orders(db.Model):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('UsersModel.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('MenuList.id'), nullable=False)
    text = db.Column(db.Text)
    title = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_for_the_order = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)

    def __init__(self, text, title, user_id, payment_for_the_order, item_id):
        self.text = text
        self.order_id = item_id
        self.title = title
        self.user_id = user_id
        self.payment_for_the_order = payment_for_the_order


class payments:
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unix = db.Column(db.Integer)
    payment_date = db.Column(db.String(30))
    username = db.Column(db.String(20))
    last_name = db.Column(db.String(30))
    payment_gross = db.Column(db.Float, )
    payment_fee = db.Column(db.Float, )
    payment_net = db.Column(db.Float)
    payer_email = db.Column(db.Float)
    payment_status = db.Column(db.String(15))
    txn_id = db.Column(db.String(25))
    content = db.relationship('Orders', backref='paid_for', lazy='joined')

    def __init__(self, unix, payment_date, username, last_name, payment_gross, payment_fee, payment_net, payment_status,
                 txn_id, payer_email):
        self.unix = unix
        self.payment_date = payment_date
        self.payment_gross = payment_gross
        self.payment_fee = payment_fee
        self.username = username
        self.last_name = last_name
        self.payment_net = payment_net
        self.payment_status = payment_status
        self.payer_email = payer_email
        self.order_that_it_payed = order_that_it_payed
        self.txn_id = txn_id


# class media(db.Model):
#     __tabelname__ = 'media'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     media_url = db.Column(db.Text)
#
#     def __init__(self, media_url):
#         self.media_url = media_url


# class Usersshema(ma.ModelSchema):
#     class Meta:
#         model = Users
#
#
# class Postsshema(ma.ModelSchema):
#     class Meta:
#         model = Posts
#
#
# class Commentsshema(ma.ModelSchema):
#     class Meta:
#         model = comments
# wa.search_index(app=app, model=Posts)
# class MyModelView(ModelView):
#     pass

class MyUsers(ModelView):
    # form_ajax_refs = {
    #     'UsersModel': {
    #         'fields': ['first_name', 'last_name', 'email'],
    #         'page_size': 10
    #     }
    # }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class MyOrders(ModelView):
    form_ajax_refs = {
        'orders': {
            'fields': ['user_id', 'text', 'title'],
            # 'page_size': 10

        }
    }


from myproject.users.form import adding_new


class MenuListView(ModelView):

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        form = adding_new()
        if form.validate_on_submit():
            item = MenuList(title=form.title.data, description=form.description.data, type=form.kind.data,
                            price=form.price.data, preparation_time=form.preparation_time.data)
            try:
                db.session.add(item)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(Markup('''<div class="alert alert-primary alert-dismissible fade show" role="alert">
   Something went wrong try again after some time 
  </div>'''))
        return self.render('adding_new_type.html', form=form, errors=form.errors)


class My_payments(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


# accessible


class My_Admin_View(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.email == 'abahormelad@gmail.com':
                return current_user.is_authenticated
        return abort(404)

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


# ------------- Admin

from myproject import admin

# admin = Admin(app)

admin.add_view(MyOrders(UsersModel, db.session, ))
admin.add_view(MyUsers(Orders, db.session, ))
admin.add_view(MenuListView(MenuList, db.session))
# admin.add_view(My_payments(payments, db.session))
