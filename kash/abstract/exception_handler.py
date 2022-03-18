from rest_framework.views import exception_handler
from exceptions_hog import exception_handler as hog_exception_handler


def custom_exception_handler(exc, context):
    try:
        response = hog_exception_handler(exc, context)
        response.data["field"] = response.data["attr"]
        del response.data["attr"]
        return response
    except:
        return exception_handler(exc, context)
