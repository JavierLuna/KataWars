from marshmallow import fields

from app import ma
from app.api.participants.schemas import ParticipantSchema
from app.models.notifications import Notification


class CreateNotificationSchema(ma.Schema):
    content = fields.Str()
    forwared_to = fields.String()


class NotificationSchema(ma.ModelSchema):
    sender = fields.Nested(ParticipantSchema)
    forwared_to = fields.Nested(ParticipantSchema)

    class Meta:
        model = Notification
