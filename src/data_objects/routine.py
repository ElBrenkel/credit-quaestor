from datetime import datetime
from marshmallow import Schema, fields, post_load
from src.data_objects.recurrence import RecurrenceType


class Routine:
    def __init__(
        self,
        time_frame: RecurrenceType,
        start_date: datetime,
        end_date: datetime,
        default_amount: float,
    ):
        self.time_frame = time_frame
        self.start_date = start_date
        self.end_date = end_date
        self.default_amount = default_amount

    def to_json(self):
        return {
            "time_frame": self.time_frame.name,
            "start_date": datetime.strftime(self.start_date, "%Y-%m-%d"),
            "end_date": datetime.strftime(self.end_date, "%Y-%m-%d"),
            "default_amount": self.default_amount,
        }


class RoutineSchema(Schema):
    time_frame = fields.Enum(RecurrenceType)
    start_date = fields.Str()
    end_date = fields.Str()
    default_amount = fields.Number()

    @post_load
    def make_routine(self, routine, **kwargs):
        routine["start_date"] = datetime.strptime(routine["start_date"], "%Y-%m-%d")
        routine["end_date"] = datetime.strptime(routine["end_date"], "%Y-%m-%d")
        return Routine(**routine)


# x = {
#     "description": "shalomiesss",
#     "amount": 354.5,
#     "transaction_date": "2024-08-19",
#     "transaction_type": "SPENDING",
# }

# sh = TransactionSchema().load(x)
# g = 1
