from app.extensions import db, ma


class Stripe(db.Model):
    __tablename__ = 'stripe'
    id = db.Column(db.Integer, primary_key=True)
    firebase_id = db.column()
    user = db.relationship("user", backref="stripe")

    subscription_id = db.Column(db.String(256), unique=False, nullable=False)
    customer_id = db.Column(db.String(256), unique=False, nullable=False)
    payment_method_id = db.Column(db.String(256), unique=False, nullable=True)
    subscription_active = db.Column(db.Boolean, default=False)
    amount = db.Column(db.Integer, unique=False)
    current_period_start = db.Column(db.Integer, unique=False)
    current_period_end = db.Column(db.Integer, unique=False)
    subscription_cancelled_at = db.Column(db.Integer, unique=False)
