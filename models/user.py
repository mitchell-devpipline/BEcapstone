import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class User(db.Model):
    __tablename__ = "User"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, first_name, last_name, phone, email, address, active):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address - address
        self.active = active


class UserSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'first_name', 'last_name', 'phone', 'email', 'address', 'active']


user_schema = UserSchema()
users_schema = UserSchema(many=True)
