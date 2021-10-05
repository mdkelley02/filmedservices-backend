from app.extensions import db
import stripe
import os

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key(STRIPE_SECRET_KEY)


class PaymentsService:
    pass
