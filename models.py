"""Data models."""
from . import db


class Startup(db.Model):

    __tablename__ = 'startups'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(255),
        index=False,
        unique=True,
        nullable=False
    )
    logo = db.Column(
        db.String(255),
        index=False,
        unique=True,
        nullable=False
    )
    oneliner = db.Column(
        db.String(255),
        index=False,
        unique=True,
        nullable=False
    )
    stage = db.Column(
        db.String(255),
        index=False,
        unique=True,
        nullable=False
    )
    industry = db.Column(
        db.String(255),
        index=False,
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return '<Startup {}>'.format(self.username)