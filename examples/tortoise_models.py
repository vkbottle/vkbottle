from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField()
    time = fields.IntField()
