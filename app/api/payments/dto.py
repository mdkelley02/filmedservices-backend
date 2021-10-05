from flask_restx import Namespace, fields


class PaymentsDto:
    api = Namespace("payments", description="payments endpoints")
    data_resp = api.model("User Data Response", {"message": fields.String})
