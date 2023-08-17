import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Orders(db.Model):
    __tablename__ = "Orders"

    order_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.user_id'), nullable=False)
    meat_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Meats.meat_id'), nullable=False)
    produce_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Produce.produce_id'), nullable=False)
    shipped = db.Column(db.Boolean(), default=True)
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, order_id, user_id, meat_id, produce_id, shipped):
        self.order_id = order_id
        self.user_id = user_id
        self.meat_id = meat_id
        self.produce_id = produce_id
        self.shipped = shipped
        self.active = True


class OrdersSchema(ma.Schema):
    class Meta:
        fields = ['']


order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)
