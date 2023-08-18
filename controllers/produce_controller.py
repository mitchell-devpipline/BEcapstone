from flask import Flask, request, jsonify

from db import *
from models.produce import Produce, produce_schema, produces_schema


def add_produce():
    req_data = request.form if request.form else request.json

    fields = ['org_id', 'produce_name', 'price']
    req_fields = ['org_id', 'produce_name', 'price']

    values = {}

    for field in fields:
        field_data = req_data.get(field)
        if field_data in req_fields and not field_data:
            return jsonify(f'{field} is required'), 400

        values[field] = field_data

    new_produce = Produce(
        # values['produce_id'],
        values['org_id'],
        values['produce_name'],
        values['price'])

    db.session.add(new_produce)
    db.session.commit()

    return jsonify('Produce Added'), 200
