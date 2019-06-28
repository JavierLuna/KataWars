from marshmallow import fields
from app import ma
from app.models.participant import Participant


class ParticipantSchema(ma.ModelSchema):
    skills = fields.List(fields.Int())
    codewars_username = fields.Str()

    class Meta:
        model = Participant
        exclude = ('_codewars_username', '_skills')
