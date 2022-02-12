from rest_framework.pagination import xLimitOffsetPagination
from rest_framework.response import Response


class KashPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.paginate = request.query_params.get("paginate")
        if not self.paginate:
            return queryset
        return super(KashPagination, self).paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        if not self.paginate:
            return Response(data)
        return super(KashPagination, self).get_paginated_response(data)
