import datetime

from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import logout_user, login_required, current_user, login_user
from markupsafe import Markup

from myproject import db
from myproject.models import UsersModel
from myproject.users.form import RegistrationForm, LoginForm
from myproject.users.handle import handle

users = Blueprint("users", __name__, template_folder="temp")


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = UsersModel.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True, duration=datetime.timedelta(weeks=52))

            nex = request.args.get('next')

            if nex is None or not nex[0] == '/':
                nex = url_for('main.index')
            return redirect(nex)
        else:
            flash(Markup('''<div class="alert alert-primary alert-dismissible fade show" role="alert">
   The password or the email is incorrect. 
  </div>'''))
            return render_template("login.html", form=form, d=form.errors)
    print(form.errors)
    return render_template('login.html', form=form, d=form.errors)


@users.route('/register', methods=["GET", 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():

        path = handle(form.profile_pic.data)
        user = UsersModel(email=form.email.data, mobile=form.mobile.data, username=form.username.data,
                          password=form.password.data,
                          path=path, employee_id=form.employee_id.data)
        try:
            print('sad as ---------------')
            db.session.add(user)
            db.session.commit()
            flash(Markup(
                '''<div class="alert alert-success" role="alert">the account has been created successfully </div>'''))
            # i can login the current user immediately or can make him has to retype his login credentials
            login_user(user)

            return redirect('/account')
        except Exception as e:
            print(e)
            # print("sad")
            db.session.rollback()
    print(form.errors)
    # print(d)
    return render_template('registration.html', form=form, d=form.errors)


@users.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/account')
@login_required
def account():
    return render_template('account.html')
