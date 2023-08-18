import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Produce(db.Model):
    __tablename__ = "Produce"

    produce_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Organization.org_id'), nullable=False)
    produce_name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, org_id, produce_name, price):
        self.org_id = org_id
        self.produce_name = produce_name
        self.price = price


class ProduceSchema(ma.Schema):
    class Meta:
        fields = ['produce_id', 'org_id', 'produce_name', 'price', 'active']


produce_schema = ProduceSchema()
produces_schema = ProduceSchema(many=True)
