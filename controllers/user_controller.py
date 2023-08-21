from flask import Flask, request, jsonify
from flask_bcrypt import generate_password_hash
from db import *
from models.user import User, user_schema, users_schema


def add_user():
    req_data = request.form if request.form else request.json

    fields = ['user_id', 'first_name', 'last_name', 'phone', 'email', 'password', 'address', 'birthday', 'active']
    req_fields = ['user_id,', 'first_name', 'last_name', 'phone', 'email', 'password', 'address']

    values = {}

    for field in fields:
        field_data = req_data.get(field)
        if field_data in req_fields and not field_data:
            return jsonify(f'{field} is required'), 400

        values[field] = field_data

    new_user = User(
        values['first_name'],
        values['last_name'],
        values['phone'],
        values['email'],
        values['password'],
        values['address'],)

    new_user.password = generate_password_hash(new_user.password).decode("utf8")
    db.session.add(new_user)
    db.session.commit()

    return jsonify('User Created'), 200
