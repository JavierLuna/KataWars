from marshmallow import fields
from app import ma
from app.models.skills import Skill


class SkillSchema(ma.ModelSchema):

    class Meta:
        model = Skill
