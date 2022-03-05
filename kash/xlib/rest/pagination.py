from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class KashPagination(LimitOffsetPagination):
    default_limit = 50

    def paginate_queryset(self, queryset, request, view=None):
        self.paginate = request.query_params.get("paginate")
        if not self.paginate:
            return queryset
        return super(KashPagination, self).paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        if not self.paginate:
            return Response(data)
        return super(KashPagination, self).get_paginated_response(data)


class CustomPagination(LimitOffsetPagination):
    default_limit = 50

    def get_paginated_response(self, data):
        return Response(data)
