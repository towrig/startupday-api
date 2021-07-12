"""Data models."""
from app import db


class Startup(db.Model):
    __tablename__ = 'startups'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(255),
        index=False,
        nullable=False
    )
    logo = db.Column(
        db.String(255),
        index=False,
        nullable=False
    )
    oneliner = db.Column(
        db.String(255),
        index=False,
        nullable=False
    )
    stage = db.Column(
        db.String(255),
        index=False,
        nullable=False
    )
    industry = db.Column(
        db.String(255),
        index=False,
        nullable=False
    )
    country = db.Column(
        db.String(255),
        index=False,
        nullable=False
    )

    def __repr__(self):
        return '<Startup {}>'.format(self.name)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
