from flask_restx import Namespace, fields


class MediaDto:
    api = Namespace("media", description="media related endpoints")
    media = api.model(
        "media object",
        {"name": fields.String, "date_created": fields.DateTime, "url": fields.String},
    )
    data_resp = api.model("media response", {})
