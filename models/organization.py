import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Organization(db.Model):
    __tablename__ = "Organization"

    org_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    produce_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Produce.produce_id'), nullable=False)
    meat_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Meats.meat_id'), nullable=False)
    org_name = db.Column(db.Integer())
    address = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, org_id, produce_id, meat_id, org_name, address, active):
        self.org_id = org_id
        self.produce_id = produce_id
        self.meat_id = meat_id
        self.org_name = org_name
        self.address = address
        self.active = active


class OrganizationSchema(ma.Schema):
    class Meta:
        fields = ['']


organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)
