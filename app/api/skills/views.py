from flask import request, abort, g

from app import db
from app.api.participants.schemas import ParticipantSchema
from app.api.skills.schemas import SkillSchema
from app.models.notifications import Notification
from app.models.participant import Participant
from app.models.skills import Skill
from .. import api_v1, auth_basic
from ..decorators import paginate, detail, json


@api_v1.route('/skill/<int:id>', methods=['POST'])
@auth_basic.login_required
@json
def activate_skill(id):
    raw_json = request.get_json()
    if 'target' not in raw_json:
        abort(401)
    target = raw_json['target']
    target = Participant.query.filter_by(username=target).first()
    if g.user.is_superuser or (target and g.user.use_skill(id)):
        skill = Skill.query.get(id)
        n = Notification(description=f"You have been targeted by: !!! {skill.name} !!!",
                         forwared_to=target, sender=g.user)
        db.session.add(g.user)
        db.session.add(n)
        try:
            db.session.commit()
        except:
            print(f"Error when user {g.user.username} tried to activate skill {skill.id} on {target.username}")
            db.session.rollback()
        return {}, 204
    abort(500)


@api_v1.route('/skill', methods=['GET'])
@paginate(SkillSchema)
def list_skills():
    return Skill.query.filter_by(visible=True)


@api_v1.route('/skill/<int:id>', methods=['GET'])
@detail(ParticipantSchema)
def detail_skills(id):
    return Skill.query.get_or_404(id)
