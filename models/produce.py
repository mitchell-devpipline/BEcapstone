import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Produce(db.Model):
    __tablename__ = "Produce"

    produce_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Organization.org_id'), nullable=False)
    produce_name = db.Column(db.String())
    price = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, produce_id, org_id, produce_name, price, active):
        self.produce_id = produce_id
        self.org_id = org_id
        self.produce_name = produce_name
        self.price = price
        self.active = active


class ProduceSchema(ma.Schema):
    class Meta:
        fields = ['']


produce_schema = ProduceSchema()
produces_schema = ProduceSchema(many=True)
