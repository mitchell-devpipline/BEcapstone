from flask import Flask, request, jsonify
from db import *
import os
from flask_marshmallow import Marshmallow

import controllers
from models.meats import Meats, meat_schema, meats_schema
from models.orders import Orders, order_schema, orders_schema
from models.organization import Organization, organization_schema, organizations_schema
from models.produce import Produce, produce_schema, produces_schema
from models.user import User, user_schema, users_schema

database_pre = os.environ.get("DATABASE_PRE")
database_addr = os.environ.get("DATABASE_ADDR")
database_user = os.environ.get("DATABASE_USER")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

org = Flask(__name__)

org.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_user}@{database_addr}:{database_port}/{database_name}"
org.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(org, db)
ma = Marshmallow(org)


def create_all():
    with org.org_context():
        print("Creating Tables")
        db.create_all()
        print("All Done")

# user


@org.route('/user/add', methods=["POST"])
def add_users():
    return controllers.add_user()


@org.route('/user/get', methods=['GET'])
def get_all_active_users():
    users = db.session.query(User).filter(users.active == True).all()

    if not users:
        return jsonify(user_schema.dump(users)), 200


@org.route("/user/get/<id>", methods=["GET"])
def get_user_by_id(id):
    user = db.session.query(user).filter(user.user_id == id).first()

    if not user:
        return jsonify("That user doesn't exit"), 404

    return jsonify(user_schema.dump(user)), 200


@org.route('/user/<uuid>', methods=['PUT'])
def update_user(uuid):
    req_data = request.form if request.form else request.json

    user = db.session.query(user).filter(user.user_id == uuid).first()

    if not user:
        return jsonify("The user doesn't exist"), 404

    for field in req_data.keys():
        if getattr(user, field):
            setattr(user, field, req_data[field])

    db.session.commit()

    return jsonify("user Updated.")


@org.route("/user/delete/<id>", methods=["DELETE"])
def del_user_by_id(id):
    user = db.session.query(user).filter(user.user_id == id).first()

    if not user:
        return jsonify("That user doesn't exit"), 404

    else:
        db.session.delete(user)
        db.session.commit()

    return jsonify("User Has been Deleted"), 200


# Sentance


if __name__ == "__main__":
    create_all()
    org.run(port=8086, host="0.0.0.0", debug=True)
