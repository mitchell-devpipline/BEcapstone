import uuid
import marshmallow as ma
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Organization(db.Model):
    __tablename__ = "Organization"

    org_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_name = db.Column(db.String(), nullable=False)
    gov_branch = db.Column(db.String(), nullable=False)
    corruption_level = db.Column(db.Integer())

    def __init__(self, org_name, gov_branch, corruption_level):
        self.org_name = org_name
        self.gov_branch = gov_branch
        self.corruption_level = corruption_level


class OrganizationSchema(ma.Schema):
    class Meta:
        fields = ['org_name', 'gov_branch', 'corruption_level']


organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)
