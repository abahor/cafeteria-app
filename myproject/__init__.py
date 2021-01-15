import os

from flask import Flask, abort
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'Cyborg'

# --------------- DATABASE
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'mykeyasdfghjklsdfghnjm'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hpprobook450g3*@localhost/cafeteria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='Lax',
# )

# --------------- BUILD
db = SQLAlchemy(app)
Migrate(app, db)


# ---------------- LOGIN
login = LoginManager()
login.init_app(app)
login.login_view = 'users.login'


class My_Admin_View(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.email == 'abahormelad@gmail.com':
                return current_user.is_authenticated
        return abort(404)

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


admin = Admin(app, index_view=My_Admin_View())

# admin.add_view(ModelView(Users, db.session))

# ----------------- REGISTER_THE_BLUEPRINT
from myproject.main.main import main  # , clever_function
from myproject.users.users import users

app.register_blueprint(users)
app.register_blueprint(main)


# app.add_url_rule('/favicon.ico',redirect_to=url_for('static',filename='icons8-social-octopus-48.png'))
# d ='/ddd'
# print(d)

@app.template_filter('r')
def r(d):
    print(type(d))
    return ''
