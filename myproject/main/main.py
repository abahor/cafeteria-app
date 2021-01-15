from datetime import time

import requests
from MySQLdb import escape_string as thwart
from flask import Blueprint, render_template, request, abort, \
    session, send_from_directory
from flask_login import login_required, current_user
from werkzeug.datastructures import ImmutableOrderedMultiDict

from myproject import db
from myproject.models import MenuList, payments, Orders

main = Blueprint('main', __name__, template_folder='temp')


@main.route('/')
@login_required
def index():
    return render_template("index.html")


@main.route('/order')
def order():
    c = request.args.get('c')
    print(c)
    print(MenuList)
    item = MenuList.query.get(c)
    print(item)
    if not item:
        abort(404)
    session['item_id'] = item.id
    session['price'] = item.price
    session['title'] = item.title
    session['description'] = item.description
    session['preparation_time'] = item.preparation_time

    return render_template('order.html', item=item, )


@main.route('/success')
def success():
    try:
        if session['paid'] != 'success':
            abort(404)
    except:
        abort(404)

    ordered = Orders(text=session['description'], title=session['title'], user_id=current_user.id,
                     payment_for_the_order=session['current_payment'], item_id=session['item_id'])
    try:
        db.session.add(ordered)
        db.session.commit()
    except:
        db.session.rollback()
        return 'something went wrong try again later'
    session['paid'] = None
    return render_template("success.html", c=session['preparation_time'])


@main.route('/ipn', methods=['POST'])
def ipn():
    try:
        arg = ""
        request.parameter_storage_class = ImmutableOrderedMultiDict
        values = request.form
        for x, y in values.iteritems():
            arg += "&{x} = {y}".format(x=x, y=y)

        validate_url = "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=notify-validate{args}".format(args=arg)
        r = requests.get(validate_url)

        if r.text == "VERIFIED":
            try:
                payer_email = thwart(request.form.get('payer_email'))
                unix = int(time.time())
                payment_date = thwart(request.form.get('payment_date'))
                username = thwart(request.form.get("custom"))
                last_name = thwart(request.form.get('last_name'))
                payment_gross = thwart(request.form.get('payment_gross'))
                if payment_gross != session['price']:
                    session['paid'] = None
                    abort(404)
                payment_fee = thwart(request.form.get("payment_fee"))
                payment_net = float(payment_gross) - float(payment_fee)
                payment_status = thwart(request.form.get('payment_status'))
                txn_id = thwart(request.form.get('txn_id'))

                payment = payments(unix=unix, payment_status=payment_status,
                                   txn_id=txn_id,
                                   payment_fee=payment_fee, payment_net=payment_net,
                                   username=username, last_name=last_name,
                                   payment_date=payment_date, payer_email=payer_email, payment_gross=payment_gross)
                try:
                    db.session.add(payment)
                    db.session.commit()
                except:
                    db.session.rollback()
                item = payments.query.filter_by(txn_id=unix).first()
                session['current_payment'] = item.id
                session['paid'] = "success"

            #     here i can update the machine to make the order
            except:
                with open('/temp/ipnput.txt', 'a') as f:
                    data = "ERROR WITH IPN DATA \n" + str(values) + '\n'
                    f.write(data)

                with open('/temp/ipnput.txt', 'a') as f:
                    data = 'SUCCESS\n' + str(values) + '\n'
                    f.write(data)

        else:
            with open('/temp/ipnput.txt', 'a') as f:
                data = "FAILURE\n" + str(values) + '\n'
                f.write(data)
        return r.text
    except Exception as e:
        return str(e)


@main.route('/menu', methods=['GET'])
def menu():
    c = request.args.get('c')
    data = ['soda', 'juice', 'coffee', 'tea', 'dessert', 'food', 'salad']
    if c not in data:
        return abort(404)
    items = MenuList.query.filter_by(type=c)
    return render_template('menu.html', items=items, )


@main.route('/counter')
def javas():
    c = request.args.get('c')
    return render_template('counter.js', c=c)


@main.route('/favicon.ico')
def favicon():
    return send_from_directory("static", filename='download (2).png'
                               , mimetype='image/vnd.microsoft.icon')
