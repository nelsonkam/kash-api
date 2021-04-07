from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(http_method_names=['GET'])
def version(request):
    return Response({
        'version': "1.0.0",
        'ios_url': "https://apple.com"
    })
