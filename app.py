from flask import Flask, request, jsonify
from db import *
import os
from flask_bcrypt import generate_password_hash, Bcrypt
from flask_marshmallow import Marshmallow

import config
import controllers
from models.meats import Meats, meat_schema, meats_schema
from models.orders import Orders, order_schema, orders_schema
from models.organization import Organization, organization_schema, organizations_schema
from models.produce import Produce, produce_schema, produces_schema
from models.user import User, user_schema, users_schema

from routes.auth_routes import auth
from routes.meats_routes import meat
from routes.order_routes import order
from routes.org_routes import org
from routes.produce_routes import produce
from routes.user_routes import user
from db import db, init_db, query

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
        seed_data()
        print("All Done")


def seed_data():
    with app.app_context():
        print("Searching for Happy Farms LLC ...")
        org_info = query(Organization).filter(
            Organization.org_name == config.org_name).first()
        if org_info:

            print(f"{config.org_name} :Here is the cayuse. Just roped it up from the back 40!")

        else:
            print(
                f"{config.org_name} Org not Found. Lemme go saddle up and find {config.org_name} in the corral...")

            org_info = Organization(
                org_name=config.org_name,
                address=config.address,
            )

            db.session.add(org_info)
            db.session.commit()

        user_name = f'{config.first_name} {config.last_name}'

        print(f"Querying for {user_name} user...")
        user_data = query(User).filter(
            User.email == config.email).first()

        if user_data == None:
            print(f"{user_name} not found! Creating {config.email} user..")

            password = os.getenv('HAPPY_FARMS_ADMIN', '')

            while not password:
                password = input(f' Enter a password for {user_name}:')

            hashed_pass = bcrypt.generate_password_hash(
                password).decode("utf8")

            record = User(
                first_name=config.first_name,
                last_name=config.last_name,
                phone=config.phone,
                email=config.email,
                password=hashed_pass,
                address=config.address,
            )

            db.session.add(record)
            db.session.commit()


app.register_blueprint(auth)
app.register_blueprint(meat)
app.register_blueprint(order)
app.register_blueprint(org)
app.register_blueprint(produce)
app.register_blueprint(user)
bcrypt = Bcrypt(app)

if __name__ == "__main__":
    create_all()
    app.run(port=8086, host="0.0.0.0", debug=True)
