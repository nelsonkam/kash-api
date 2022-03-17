from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_400_BAD_REQUEST and isinstance(
            response.data, dict
        ):
            result = {}
            for key, value in response.data.items():
                result[key] = value[0] if isinstance(value, list) else value
            response.data = result

    return response
