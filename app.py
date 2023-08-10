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

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_user}@{database_addr}:{database_port}/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
ma = Marshmallow(app)


def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("All Done")


# Orgs

@app.route('/orgs/add', methods=["POST"])
def add_organization():
    return controllers.add_organization()


@app.route('/orgs/get', methods=['GET'])
def get_all_active_orgs():
    orgs = db.session.query(Organization).all()
    if not orgs:
        return jsonify("there are no orgs here"), 404
    else:
        return jsonify(organizations_schema.dump(orgs)), 200


@app.route("/org/get/<id>", methods=["GET"])
def get_org_by_id(id):
    org_record = db.session.query(Organization).filter(Organization.org_id == id).first()

    if not org_record:
        return jsonify("That organization doesn't exit"), 404

    return jsonify(organization_schema.dump(org_record)), 200


@app.route('/org/<uuid>', methods=['PUT'])
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


@app.route("/org/delete/<id>", methods=["DELETE"])
def del_org_by_id(id):
    org_record = db.session.query(Organization).filter(Organization.org_id == id).first()

    if not org_record:
        return jsonify("That organization doesn't exit"), 404

    else:
        db.session.delete(org_record)
        db.session.commit()

    return jsonify("Organization Deleted"), 200


# user

@app.route('/user/add', methods=["POST"])
def add_users():
    return controllers.add_user()


@app.route('/user/get', methods=['GET'])
def get_all_active_users():
    users = db.session.query(User).filter(users.active == True).all()

    if not users:
        return jsonify(user_schema.dump(users)), 200


@app.route("/user/get/<id>", methods=["GET"])
def get_user_by_id(id):
    user = db.session.query(user).filter(user.user_id == id).first()

    if not user:
        return jsonify("That user doesn't exit"), 404

    return jsonify(user_schema.dump(user)), 200


@app.route('/user/<uuid>', methods=['PUT'])
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


@app.route("/user/delete/<id>", methods=["DELETE"])
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
    app.run(port=8086, host="0.0.0.0", debug=True)
