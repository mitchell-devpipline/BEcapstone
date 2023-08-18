import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Organization(db.Model):
    __tablename__ = "Organization"

    org_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_name = db.Column(db.String())
    address = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True)

    def __init__(self, org_name, address):
        self.org_name = org_name
        self.address = address
        self.active = True


class OrganizationSchema(ma.Schema):
    class Meta:
        fields = ['org_id', 'org_name', 'address', 'active']


organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)
