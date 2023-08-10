from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

__all__ = ('db', 'init_db')

db = SQLAlchemy()


def init_db(org=None, db=None):
    if isinstance(org, Flask) and isinstance(db, SQLAlchemy):
        db.init_org(org)

    else:
        raise ValueError("Cannot init DB wihtout db and org objects")
