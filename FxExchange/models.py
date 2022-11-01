from . import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    from_currency = db.Column(db.String(500))
    to_currency = db.Column(db.String(500))
    amount_to_convert = db.Column(db.String(500))
    current_rate = db.Column(db.String(500))
    timestamp = db.Column(db.String(500))
    converted_amount = db.Column(db.String(500))


    def __init__(self, from_currency, to_currency, amount_to_convert, current_rate, timestamp, converted_amount ):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.amount_to_convert = amount_to_convert
        self.current_rate = current_rate
        self.timestamp = timestamp
        self.converted_amount = converted_amount
 