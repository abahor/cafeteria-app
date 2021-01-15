from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from markupsafe import Markup
from wtforms import StringField, SubmitField, FloatField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired, length, ValidationError

from myproject.models import UsersModel


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField("Login")


def check_email(self, args):
    user = UsersModel.query.filter_by(email=self.email.data).first()
    print(self.email.data)
    if user:
        raise ValidationError((Markup('''
   This email already exist try <strong><a href="/login">login</a></strong> instead.''')))


def validate_username(self, field):
    excluded_chars = " *?!'^+%&/()=}][{$#"
    for char in self.username.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed in username.")


def check_employee(self, args):
    employee = UsersModel.query.filter_by(employee_id=self.employee_id.data).first()
    print(self.email.data)
    if employee:
        raise ValidationError((Markup('''
       There is an account who is registered with this ID
      ''')))


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(), check_email], render_kw={'placeholder': 'Email'})
    username = StringField('Username', validators=[InputRequired(), validate_username],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('Password',
                             validators=[InputRequired(), EqualTo('pass_confirm', message='Passwords must match')],
                             render_kw={'placeholder': 'Password'})
    pass_confirm = PasswordField('Confirm Password',
                                 validators=[InputRequired()], render_kw={'placeholder': 'confirm password'})
    mobile = StringField("Phone Argument", validators=[InputRequired()], render_kw={"placeholder": "phone number"})
    employee_id = StringField('Username', validators={InputRequired(), check_employee},
                              render_kw={'placeholder': 'Employee ID'})
    profile_pic = FileField('Upload your ID', validators=[InputRequired(),
                                                          FileAllowed(['jpeg', 'png', 'jpg'],
                                                                      message='only a jpg or png '
                                                                              'format is accepted')])
    submit = SubmitField('Register')


class Num(FloatField):
    msg = ""

    def __init__(self, label=None, validators=None, msg=None, **kwargs):
        super(FloatField, self).__init__(label, validators, **kwargs)
        self.msg = msg

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0])
            except ValueError:
                self.data = None
                if self.msg:
                    raise ValueError(self.gettext(self.msg))
                else:
                    raise ValueError(self.gettext('The value of the price has to be a number'))


class adding_new(FlaskForm):
    title = StringField("Name of the meal",
                        validators=[InputRequired(), length(min=1, max=64, message='the name of the meal is too long')],
                        render_kw={'placeholder': 'Name'})
    description = TextAreaField('Description of the item and its content',
                                validators=[InputRequired()], render_kw={'placeholder': 'Description of the meal'})
    price = Num('Enter the price of the item', validators=[InputRequired()], render_kw={'placeholder': 'Price'})
    kind = SelectField(u'Type of the food',
                       choices=[('food', 'Food'), ('soda', 'Soda'), ('juice', 'Juice'),
                                ('coffee', 'Coffee'), ('tea', 'Tea'), ('dessert', 'Dessert')],
                       validators=[InputRequired()])
    preparation_time = Num("Enter the average time it take to prepare this meal in minutes",
                           msg="Enter the time it take to prepare this meal in minutes ",
                           validators=[InputRequired()], render_kw={'placeholder': 'Time in minutes'})
    submit = SubmitField('Add')
