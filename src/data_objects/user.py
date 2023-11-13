from marshmallow import Schema, fields, post_load


# Define a User class
class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name

    def to_json(self):
        return {"id": self.user_id, "name": self.name}


# Define a schema using Marshmallow
class UserSchema(Schema):
    user_id = fields.Str()
    name = fields.Str()

    @post_load
    def make_user(self, user, **kwargs):
        return User(**user)


#
