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


if __name__ == "__main__":
    create_all()
    app.run(port=8086, host="0.0.0.0", debug=True)
