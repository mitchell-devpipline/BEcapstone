from flask import Flask, request, jsonify

from db import *
from models.organization import Organization, organization_schema, organizations_schema


def add_organization():
    req_data = request.form if request.form else request.json

    fields = ['org_id', 'produce_id', 'meat_id', 'org_name', 'address']
    req_fields = ['org_id', 'produce_id', 'meat_id', 'org_name']

    values = {}

    for field in fields:
        field_data = req_data.get(field)
        if field_data in req_fields and not field_data:
            return jsonify(f'{field} is required'), 400

        values[field] = field_data

    new_org = Organization(values['produce_id'], values['meat_id'], values['org_name'], values['address'])
    db.session.add(new_org)
    db.session.commit()

    return jsonify('Organization Created'), 200
