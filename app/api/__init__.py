from flask import Blueprint, g
from flask_httpauth import HTTPTokenAuth

from app.models.participant import Participant

api_v1 = Blueprint('v1', __name__)
auth_basic = HTTPTokenAuth(scheme='Bearer')
auth_super = HTTPTokenAuth(scheme='Bearer')


@auth_basic.verify_token
def verify_basic_token(token):
    participant = Participant.verify_auth_token(token)
    if participant:
        g.user = participant
        g.token = token
        return True
    return False


@auth_super.verify_token
def verify_super_token(token):
    participant = Participant.verify_auth_token(token)
    if participant and participant.is_superuser:
        g.user = participant
        g.token = token
        return True
    return False


from . import participants, notifications, skills, auth
