from tortoise import fields
from tortoise.models import Model


"""
Simple User model with tortoise orm
"""
class User(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField()
    time = fields.IntField()

    class Meta:
        database = "user"


"""
A model was made to work with DatabaseBranch manager
Three fields are required: uid as integer, branch as string (near 20 symbols max)
and context as string (as big as possible) to store context json
"""
class UserState(Model):
    id = fields.IntField(pk=True)  # Primary key is often recommended
    uid = fields.IntField()
    branch = fields.CharField(20)
    context = fields.CharField(255)

    class Meta:
        database = "user_state"
