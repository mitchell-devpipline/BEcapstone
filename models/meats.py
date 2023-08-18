import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Meats(db.Model):
    __tablename__ = "Meats"

    meat_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Organization.org_id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, meat_id, org_id, name, price):
        self.meat_id = meat_id
        self.org_id = org_id
        self.name = name
        self.price = price
        self.active = True


class MeatSchema(ma.Schema):
    class Meta:
        fields = ['meat_id', 'org_id', 'name', 'price', 'active']


meat_schema = MeatSchema()
meats_schema = MeatSchema(many=True)
