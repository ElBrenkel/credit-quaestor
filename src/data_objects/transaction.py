from marshmallow import Schema, fields, post_load


class Transaction:
    def __init__(self, description, amount):
        self.description = description
        self.amount = amount


# Define a schema using Marshmallow
class TransactionSchema(Schema):
    description = fields.Str()
    amount = fields.Number()

    @post_load
    def make_transaction(self, transaction, **kwargs):
        return Transaction(**transaction)
