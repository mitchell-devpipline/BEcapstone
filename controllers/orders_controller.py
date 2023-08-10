from flask import Flask, request, jsonify

from db import *
from models.orders import Orders, order_schema, orders_schema


def add_order():
    req_data = request.form if request.form else request.json

    fields = ['order_id', 'user_id', 'meat_id', 'produce_id', 'shipped']
    req_fields = ['order_id', 'user_id', 'meat_id', 'produce_id', 'shipped']

    values = {}

    for field in fields:
        field_data = req_data.get(field)
        if field_data in req_fields and not field_data:
            return jsonify(f'{field} is required'), 400

        values[field] = field_data

    new_produce = Orders(
        values['order_id'],
        values['user_id'],
        values['meat_id'],
        values['produce_id'],
        values['shipped'],
        values['active'])

    db.session.add(new_produce)
    db.session.commit()

    return jsonify('Order Added'), 200
