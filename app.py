from flask import Flask, request, jsonify
from db import *
import os
from flask_marshmallow import Marshmallow

import controllers
from models.people import People, person_schema, people_schema
from models.organization import Organization, organization_schema, organizations_schema
from models.sentance import Sentance, sentance_schema, sentances_schema
from models.crimes import Crimes, crime_schema, crimes_schema
from models.crime_categories import CrimeCategories, crimecat_schema, crimecats_schema

database_pre = os.environ.get("DATABASE_PRE")
database_addr = os.environ.get("DATABASE_ADDR")
database_person = os.environ.get("DATABASE_USER")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_person}@{database_addr}:{database_port}/{database_name}"
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


# People

@app.route('/person/add', methods=["POST"])
def add_person():
    return controllers.add_person()


@app.route('/persons/get', methods=['GET'])
def get_all_active_persons():
    persons = db.session.query(People).filter(People.active == True).all()

    if not persons:
        return jsonify(person_schema.dump(persons)), 200


@app.route("/person/get/<id>", methods=["GET"])
def get_persons_by_id(id):
    person = db.session.query(People).filter(People.person_id == id).first()

    if not person:
        return jsonify("That person doesn't exit"), 404

    return jsonify(person_schema.dump(person)), 200


@app.route('/person/<uuid>', methods=['PUT'])
def update_person(uuid):
    req_data = request.form if request.form else request.json

    person = db.session.query(People).filter(People.person_id == uuid).first()

    if not person:
        return jsonify("The person doesn't exist"), 404

    for field in req_data.keys():
        if getattr(person, field):
            setattr(person, field, req_data[field])

    db.session.commit()

    return jsonify("person Updated.")


@app.route("/person/delete/<id>", methods=["DELETE"])
def del_person_by_id(id):
    person = db.session.query(People).filter(People.person_id == id).first()

    if not person:
        return jsonify("That person doesn't exit"), 404

    else:
        db.session.delete(person)
        db.session.commit()

    return jsonify("person Has been Deleted"), 200


# Sentance


if __name__ == "__main__":
    create_all()
    app.run(port=8086, host="0.0.0.0", debug=True)
