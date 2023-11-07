from marshmallow import Schema, fields, post_load
from transaction import TransactionSchema


# Define a User class
class User:
    def __init__(self, phone, email, monthly_earnings, monthly_spendings):
        self.phone = phone
        self.email = email
        self.single_earnings = []
        self.monthly_earnings = monthly_earnings
        self.single_spendings = []
        self.monthly_spendings = monthly_spendings


# Define a schema using Marshmallow
class UserSchema(Schema):
    phone = fields.Str()
    email = fields.Email()
    single_earnings = fields.List(fields.Nested(TransactionSchema), required=False)
    monthly_earnings = fields.Number()
    single_spendings = fields.List(fields.Nested(TransactionSchema), required=False)
    monthly_spendings = fields.Number()

    @post_load
    def make_user(self, user, **kwargs):
        return User(**user)


#
