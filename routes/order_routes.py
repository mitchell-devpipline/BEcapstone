from flask import Flask, request, jsonify, Blueprint
from db import *
import os
from flask_marshmallow import Marshmallow
from controllers import orders_controller
from models.orders import Orders, order_schema, orders_schema
order = Blueprint('order', __name__)


@order.route('/order/add', methods=["POST"])
def add_order():
    return orders_controller.add_order()


@order.route('/order/get', methods=['GET'])
def get_all_active_order():
    orders = db.session.query(Orders).filter(Orders.active == True).all()

    if orders:
        return jsonify(orders_schema.dump(orders)), 200

    else:
        return jsonify("There are no orders that have been placed"), 404


@order.route("/order/get/<id>", methods=["GET"])
def get_order_by_id(id):
    order = db.session.query(Orders).filter(Orders.order_id == id).first()

    if not order:
        return jsonify("That order doesn't exit"), 404

    return jsonify(order_schema.dump(order)), 200


@order.route('/order/<uuid>', methods=['PUT'])
def update_order(uuid):
    req_data = request.form if request.form else request.json

    order = db.session.query(Orders).filter(Orders.order_id == uuid).first()

    if not order:
        return jsonify("The order doesn't exist"), 404

    for field in req_data.keys():
        if getattr(order, field):
            setattr(order, field, req_data[field])

    db.session.commit()

    return jsonify("order Updated.")


@order.route("/order/delete/<id>", methods=["DELETE"])
def del_order_by_id(id):
    order = db.session.query(Orders).filter(Orders.order_id == id).first()

    if not order:
        return jsonify("That order doesn't exit"), 404

    else:
        db.session.delete(order)
        db.session.commit()

    return jsonify("Order Has been Deleted"), 200
