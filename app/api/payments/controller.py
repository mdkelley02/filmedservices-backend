from flask_restx import Resource, reqparse
from flask import request

# from .services import PaymentsService
from .dto import PaymentsDto
import os
import stripe
from app.api.auth.services import AuthService


api = PaymentsDto.api
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
client_url = os.getenv("CLIENT_URL")


@api.route("/config")
class Config(Resource):
    def get(self):
        return "config"


@api.route("/subscriptions")
class Subscriptions(Resource):
    def get(self):
        products = {
            "PHOTO_PLAN": os.getenv("STRIPE_PHOTO_PLAN"),
            "VIDEO_PLAN": os.getenv("STRIPE_VIDEO_PLAN"),
            "SOCIAL_MEDIA_PLAN": os.getenv("STRIPE_SOCIAL_MEDIA_PLAN"),
        }

        return [
            dict(
                **stripe.Product.retrieve(product_id),
                price=stripe.Price.retrieve(
                    stripe.Price.list(product=product_id).data[0]["id"]
                )
            )
            for product_id in products.values()
        ]


@api.route("/customer")
class Customer(Resource):
    def post(self, **kwargs):
        pass


@api.route("/create-checkout-session")
class CreateCheckoutSession(Resource):
    def post(self):
        checkout_session_parser = reqparse.RequestParser()
        checkout_session_parser.add_argument("product_id", required=True)

        args = checkout_session_parser.parse_args()
        product_id = args["product_id"]
        try:
            price = stripe.Price.list(product=product_id)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price.data[0]["id"],
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                success_url=client_url,
                cancel_url=client_url + "/subscriptions",
            )
            return checkout_session, 200
        except Exception as e:
            print(e)
            return "Server error", 500


@api.route("/test")
class Test(Resource):
    def get(self):
        return "test"


@api.route("/webhook")
class Webhook(Resource):
    def post(self):
        print("fuqin hit")
        endpoint_secret = "whsec_OInrPavAZ7flaBFFN1gFgtIIlmAPVrCq"
        event = None
        payload = request.data
        sig_header = request.headers["STRIPE_SIGNATURE"]
        print(payload)
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            raise e
        except stripe.error.SignatureVerificationError as e:
            raise e
        if event["type"] == "payment_intent.succeeded":
            intent = event["data"]["object"]
            print(intent)
            print("################", intent["customer"])
        else:
            print("Unhandled event type {}".format(event["type"]))
