from flask import request, Blueprint
from flask import Flask, request, jsonify
from db import *
import os
from flask_marshmallow import Marshmallow
from models.organization import Organization, organizations_schema, organization_schema

from controllers import organization_controller

org = Blueprint('org', __name__)

# Orgs


@org.route('/orgs/add', methods=["POST"])
def add_organization():
    return organization_controller.add_organization()


@org.route('/orgs/get', methods=['GET'])
def get_all_active_orgs():
    orgs = db.session.query(Organization).all()
    if not orgs:
        return jsonify("there are no orgs here"), 404
    else:
        return jsonify(organizations_schema.dump(orgs)), 200


@org.route("/org/get/<id>", methods=["GET"])
def get_org_by_id(id):
    org_record = db.session.query(Organization).filter(Organization.org_id == id).first()

    if not org_record:
        return jsonify("That organization doesn't exit"), 404

    return jsonify(organization_schema.dump(org_record)), 200


@org.route('/org/<uuid>', methods=['PUT'])
def update_org(uuid):
    req_data = request.form if request.form else request.json

    org = db.session.query(Organization).filter(Organization.org_id == uuid).first()

    if not org:
        return jsonify("The organization doesn't exist"), 404

    for field in req_data.keys():
        if getattr(org, field):
            setattr(org, field, req_data[field])

    db.session.commit()

    return jsonify("Organization Updated.")


@org.route("/org/delete/<id>", methods=["DELETE"])
def del_org_by_id(id):
    org_record = db.session.query(Organization).filter(Organization.org_id == id).first()

    if not org_record:
        return jsonify("That organization doesn't exit"), 404

    else:
        db.session.delete(org_record)
        db.session.commit()

    return jsonify("Organization Deleted"), 200
