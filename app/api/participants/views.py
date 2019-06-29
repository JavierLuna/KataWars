from flask import g, abort

from app.api.participants.schemas import ParticipantSchema
from app.models.participant import Participant
from .. import api_v1, auth_basic
from ..decorators import paginate, detail, json


@api_v1.route('/participant/me', methods=['GET'])
@auth_basic.login_required
@detail(ParticipantSchema)
def me_participant():
    return Participant.query.get(g.user.id)


@api_v1.route('/participant', methods=['GET'])
@auth_basic.login_required
@json
def list_participants():
    return [participant.username for participant in Participant.query.filter_by(is_superuser=False).all()]


@api_v1.route('/participant/<int:id>', methods=['GET'])
@auth_basic.login_required
@detail(ParticipantSchema)
def detail_participants(id):
    if g.user.is_superuser:
        return Participant.query.get_or_404(id)
    else:
        if g.user.id == id:
            return g.user
        abort(404)
