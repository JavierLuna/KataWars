import random
from app import db


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    probability = db.Column(db.Float)

    visible = db.Column(db.Boolean, default=True)

    def can_consume(self, user):
        return random.random() > self.probability
