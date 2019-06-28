import json
import uuid
from typing import List

import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(120), unique=True, nullable=False)
    received_notifications = db.relationship('Notification', lazy='dynamic', backref=db.backref('forwared_to'),
                                             foreign_keys='notifications.c.forwared_to_id')
    sent_notifications = db.relationship('Notification', lazy='dynamic', backref=db.backref('sender'),
                                         foreign_keys='notifications.c.sender_id')

    score = db.Column(db.Integer, default=0)
    completed_challenges = db.Column(db.Integer, default=0)

    password_hash = db.Column(db.Text(), nullable=False)

    is_superuser = db.Column(db.Boolean, default=False)

    _codewars_username = db.Column(db.String(120))
    _skills = db.Column(db.String(900), default='[]')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, version=None):
        token = {'id': self.id, 'entropy': str(uuid.uuid4())}
        if version:
            token['api_version'] = version
        encoded = jwt.encode(token, current_app.config['SECRET_KEY'], algorithm='HS256')
        return encoded

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return None
        participant = Participant.query.get(data['id'])
        return participant

    def use_skill(self, skill_id: int):
        if skill_id not in self.skills:
            return False
        skills = self.skills
        skills.remove(skill_id)
        self.skills = skills
        return True

    def add_skill(self, skill_id: int):
        skills = self.skills
        skills.append(skill_id)
        self.skills = skills

    @property
    def skills(self) -> List[int]:
        return json.loads(self._skills)

    @skills.setter
    def skills(self, new_skills):
        self._skills = json.dumps(new_skills)

    @property
    def codewars_username(self):
        return self._codewars_username if self._codewars_username else self.username
