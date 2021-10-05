def make_response(message, response_code, event=""):
    return {
        "message": message,
        "event": event
    }, response_code
