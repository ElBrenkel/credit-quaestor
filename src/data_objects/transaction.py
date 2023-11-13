from datetime import datetime
from marshmallow import Schema, fields, post_load
from transaction_type import TransactionType


class Transaction:
    def __init__(
        self,
        description,
        amount,
        transaction_type: TransactionType,
        transaction_date=datetime.utcnow(),
    ):
        self.description = description
        self.amount = amount
        self.transaction_date = transaction_date
        self.transaction_type = transaction_type

    def to_json(self):
        return {
            "amount": self.amount,
            "description": self.description,
            "transaction_type": self.transaction_type.name,
            "transaction_date": datetime.strftime(self.transaction_date, "%Y-%m-%d"),
        }


class TransactionSchema(Schema):
    description = fields.Str()
    amount = fields.Number()
    transaction_date = fields.Str(required=False)
    transaction_type = fields.Enum(TransactionType)

    @post_load
    def make_transaction(self, transaction, **kwargs):
        if transaction["transaction_date"]:
            transaction["transaction_date"] = datetime.strptime(
                transaction["transaction_date"], "%Y-%m-%d"
            )
        return Transaction(**transaction)


# x = {
#     "description": "shalomiesss",
#     "amount": 354.5,
#     "transaction_date": "2024-08-19",
#     "transaction_type": "SPENDING",
# }

# sh = TransactionSchema().load(x)
# g = 1
