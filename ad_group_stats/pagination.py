from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CampaignPerformancePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def paginate_and_respond(self, queryset, serializer_class, request, many=True):
        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = serializer_class(page, many=many)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=many)
        return Response(serializer.data)

    def get_paginated_response(self, data):
        return Response(
            {
                'message': 'successful',
                'previous': self.get_previous_link(),
                'next': self.get_next_link(),
                'count': self.page.paginator.count,
                'data': data,
            }
        )
