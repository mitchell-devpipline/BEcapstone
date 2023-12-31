from flask import Flask, request, jsonify, Blueprint
from db import *
import os
from flask_marshmallow import Marshmallow
from controllers import user_controller
from models.user import User, user_schema, users_schema

user = Blueprint('user', __name__)


@user.route('/user/add', methods=["POST"])
def add_users():
    return user_controller.add_user()


@user.route('/user/get', methods=['GET'])
def get_all_active_users():
    users = db.session.query(User).filter(User.active == True).all()

    if users:
        return jsonify(users_schema.dump(users)), 200


@user.route("/user/get/<id>", methods=["GET"])
def get_user_by_id(id):
    user = db.session.query(User).filter(User.user_id == id).first()

    if not user:
        return jsonify("That user doesn't exit"), 404

    return jsonify(user_schema.dump(user)), 200


@user.route('/user/<uuid>', methods=['PUT'])
def update_user(uuid):
    req_data = request.form if request.form else request.json

    user = db.session.query(User).filter(User.user_id == uuid).first()

    if not user:
        return jsonify("The user doesn't exist"), 404

    for field in req_data.keys():
        if getattr(user, field):
            setattr(user, field, req_data[field])

    db.session.commit()

    return jsonify("user Updated.")


@user.route("/user/delete/<id>", methods=["DELETE"])
def del_user_by_id(id):
    user = db.session.query(User).filter(User.user_id == id).first()

    if not user:
        return jsonify("That user doesn't exit"), 404

    else:
        db.session.delete(user)
        db.session.commit()

    return jsonify("User Has been Deleted"), 200
