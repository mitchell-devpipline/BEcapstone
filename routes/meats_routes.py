from flask import Flask, request, jsonify, Blueprint
from db import *
import os
from flask_marshmallow import Marshmallow
from controllers import meats_controller
from models.meats import Meats, meat_schema, meats_schema
meat = Blueprint('meat', __name__)


@meat.route('/meat/add', methods=["POST"])
def add_meat():
    return meats_controller.add_meat()


@meat.route('/meat/get', methods=['GET'])
def get_all_active_meat():
    meats = db.session.query(Meats).filter(meats.active == True).all()

    if not meats:
        return jsonify(meat_schema.dump(meats)), 200


@meat.route("/meat/get/<id>", methods=["GET"])
def get_meat_by_id(id):
    meat = db.session.query(meat).filter(meat.user_id == id).first()

    if not meat:
        return jsonify("That Meat doesn't exit"), 404

    return jsonify(meat_schema.dump(meat)), 200


@meat.route('/meat/<uuid>', methods=['PUT'])
def update_meat(uuid):
    req_data = request.form if request.form else request.json

    meat = db.session.query(meat).filter(meat.user_id == uuid).first()

    if not meat:
        return jsonify("The Meat doesn't exist"), 404

    for field in req_data.keys():
        if getattr(meat, field):
            setattr(meat, field, req_data[field])

    db.session.commit()

    return jsonify("meat Updated.")


@meat.route("/meat/delete/<id>", methods=["DELETE"])
def del_meat_by_id(id):
    meat = db.session.query(meat).filter(meat.user_id == id).first()

    if not meat:
        return jsonify("That Meat doesn't exit"), 404

    else:
        db.session.delete(meat)
        db.session.commit()

    return jsonify("Meat Has been Deleted"), 200
