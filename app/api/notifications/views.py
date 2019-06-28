from flask import g, abort, request
from sqlalchemy import or_

from app import db
from app.api.notifications.schemas import NotificationSchema, CreateNotificationSchema
from app.models.notifications import Notification
from app.models.participant import Participant
from .. import api_v1, auth_basic, auth_super
from ..decorators import paginate, detail, json


@api_v1.route('/notification', methods=['GET'])
@auth_basic.login_required
@paginate(NotificationSchema)
def list_notifications():
    query = Notification.query
    if not g.user.is_superuser:
        query = query.filter(or_(Notification.sender_id == g.user.id, Notification.forwared_to_id == g.user.id))

    return query


@api_v1.route('/notification/<int:id>', methods=['GET'])
@auth_basic.login_required
@detail(NotificationSchema)
def detail_notification(id):
    query = Notification.query.filter_by(id=id)

    if not g.user.is_superuser:
        query = query.filter(or_(Notification.sender_id == g.user.id, Notification.forwared_to_id == g.user.id))

    result = query.first()
    if not result:
        abort(404)
    return result


@api_v1.route('/notification', methods=['POST'])
@auth_super.login_required
@json
def create_notification():
    raw_json = request.get_json()
    schema = CreateNotificationSchema()
    results = schema.load(raw_json)
    if results.errors:
        raise Exception("Validation errors:", results.errors)
    n = Notification(sender=g.user, forwared_to=Participant.query.filter_by(username=results.data['forwared_to']),
                     description=results.data['content'])
    db.session.add(n)
    try:
        db.session.commit()
        return {}, 204
    except:
        print("Error creating notification", results.data)
        db.session.rollback()
        abort(500)


@api_v1.route('/notification/all', methods=['POST'])
@auth_super.login_required
@json
def create_notification_all():
    raw_json = request.get_json()
    if 'content' in raw_json:
        content = raw_json['content']
    else:
        abort(401)

    for participant in Participant.query.filter_by(is_superuser=False).all():

        n = Notification(sender=g.user, forwared_to=participant,
                         description=content)
        db.session.add(n)
        try:
            db.session.commit()
            return {}, 204
        except:
            print("Error creating notification", content)
            db.session.rollback()
            abort(500)
