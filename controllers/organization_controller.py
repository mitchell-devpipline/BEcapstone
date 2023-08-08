from flask import Flask, request, jsonify

from db import *
from models.organization import Organization, organization_schema, organizations_schema


def add_organization():
    req_data = request.form if request.form else request.json

    fields = ['name', 'phone', 'city', 'state', 'active']
    req_fields = ['name']

    values = {}

    for field in fields:
        field_data = req_data.get(field)
        if field_data in req_fields and not field_data:
            return jsonify(f'{field} is required'), 400

        values[field] = field_data

    new_org = Organization(values['name'], values['city'], values['state'], values['phone'], values['active'])
    db.session.add(new_org)
    db.session.commit()

    return jsonify('Organization Created'), 200
