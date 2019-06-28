from flask import g, abort

from app.api.participants.schemas import ParticipantSchema
from app.models.participant import Participant
from .. import api_v1, auth_basic
from ..decorators import paginate, detail


@api_v1.route('/participant/me', methods=['GET'])
@auth_basic.login_required
@detail(ParticipantSchema)
def me_participant():
    return Participant.query.get(g.user.id)


@api_v1.route('/participant', methods=['GET'])
@auth_basic.login_required
@paginate(ParticipantSchema)
def list_participants():
    if g.user.is_superuser:
        return Participant.query.filter_by(is_superuser=False)
    else:
        return Participant.query.filter_by(username=g.user.username)


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
