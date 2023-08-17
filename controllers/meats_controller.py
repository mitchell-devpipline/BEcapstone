from flask import Flask, request, jsonify

from db import *
from models.meats import Meats, meat_schema, meats_schema


def add_meat():
    req_data = request.form if request.form else request.json

    fields = ['meat_id', 'org_id', 'name', 'price', 'active']
    req_fields = ['meat_id', 'org_id', 'name', 'price', 'active']

    values = {}

    for field in fields:
        field_data = req_data.get(field)
        if field_data in req_fields and not field_data:
            return jsonify(f'{field} is required'), 400

        values[field] = field_data

    new_meat = Meats(
        values['meat_id'],
        values['org_id'],
        values['name'],
        values['price'])

    db.session.add(new_meat)
    db.session.commit()

    return jsonify('Meat Added'), 200
