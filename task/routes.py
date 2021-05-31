from flask import Flask, Response, request, jsonify, make_response, render_template, url_for, flash, session, redirect
from task import session, engine, app
import pprint
from threading import Timer
import requests
import json
from datetime import datetime, timedelta
from .models import Invoice
import hashlib


@app.route('/', methods=['GET', 'POST'])
def data():

    if request.method == 'POST':

        amount = dict(request.form).get('amount')
        description = dict(request.form).get('description')
        currency = dict(request.form).get('payment_currency')

        invoice = Invoice(currency=currency, sum=amount, description=description)
        session.add(invoice)
        session.commit()

        shop_id = 5

        if dict(request.form).get('payment_currency') == 'EUR':

            dictionary = {
                'currency': 840,
                'amount': amount,
                'shop_id': shop_id,
                'shop_order_id': invoice.id,
                'description': description,
            }

            sign = cipher(dictionary)

            dictionary.update({'sign': sign})

            return render_template('EUR.html', dictionary=dictionary)

        elif dict(request.form).get('payment_currency') == 'USD' and len(dict(request.form).get('amount')) < 6:

            dictionary = {
                'shop_amount': amount,
                'shop_currency': 840,
                'shop_order_id': invoice.id,
                'payer_currency': 840,
                'shop_id ': shop_id
            }

            sign = cipher(dictionary)

            response = requests.post('https://core.piastrix.com/bill/create',
                                     json={
                                        "description": description,
                                        "payer_currency": dictionary['payer_currency'],
                                        "shop_amount": amount,
                                        "shop_currency": dictionary['shop_currency'],
                                        "shop_id": shop_id,
                                        "shop_order_id": invoice.id,
                                        "sign": sign,
                                     }, timeout=1)

            return redirect(response.json()['data']['url'], code=302) if response.status_code == 200 else\
                Response(status=201)

        elif dict(request.form).get('payment_currency') == 'RUB':

            dictionary = {
                'currency': 643,
                'amount': amount,
                'payway': 'advcash_rub',
                'shop_id': shop_id,
                'shop_order_id': invoice.id
            }

            sign = cipher(dictionary)

            response = requests.post('https://core.piastrix.com/invoice/create',
                                     json={
                                         "currency": dictionary['currency'],
                                         "sign": sign,
                                         "payway": dictionary['payway'],
                                         "amount": dictionary['amount'],
                                         "shop_id": shop_id,
                                         "shop_order_id": invoice.id,
                                         "description": description,
                                     }, timeout=1)

            return render_template('RUB.html', data=response.json()['data'])

    return render_template('base.html')


def cipher(dictionary):

    cipher_string = ":".join([str(x[1]) for x in sorted(dictionary.items())]) + 'SecretKey01'
    sign = hashlib.sha256(bytes(cipher_string, "utf-8")).hexdigest()

    return sign
