from flask import Flask, request, jsonify, Blueprint
from db import *
import os
from flask_marshmallow import Marshmallow
from controllers import produce_controller
from models.produce import produce, produce_schema, produces_schema
produce = Blueprint('produce', __name__)


@produce.route('/produce/add', methods=["POST"])
def add_produce():
    return produce_controller.add_produce()


@produce.route('/produce/get', methods=['GET'])
def get_all_active_produce():
    produces = db.session.query(produces).filter(produces.active == True).all()

    if not produces:
        return jsonify(produce_schema.dump(produces)), 200


@produce.route("/produce/get/<id>", methods=["GET"])
def get_produce_by_id(id):
    produce = db.session.query(produce).filter(produce.user_id == id).first()

    if not produce:
        return jsonify("That produce doesn't exit"), 404

    return jsonify(produce_schema.dump(produce)), 200


@produce.route('/produce/<uuid>', methods=['PUT'])
def update_produce(uuid):
    req_data = request.form if request.form else request.json

    produce = db.session.query(produce).filter(produce.user_id == uuid).first()

    if not produce:
        return jsonify("The produce doesn't exist"), 404

    for field in req_data.keys():
        if getattr(produce, field):
            setattr(produce, field, req_data[field])

    db.session.commit()

    return jsonify("produce Updated.")


@produce.route("/produce/delete/<id>", methods=["DELETE"])
def del_produce_by_id(id):
    produce = db.session.query(produce).filter(produce.user_id == id).first()

    if not produce:
        return jsonify("That produce doesn't exit"), 404

    else:
        db.session.delete(produce)
        db.session.commit()

    return jsonify("produce Has been Deleted"), 200
