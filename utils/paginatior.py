from collections import OrderedDict

from django.core.paginator import InvalidPage
from rest_framework import pagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class PagePagination(pagination.PageNumberPagination):

    page_size = 10
    page_query_param = "currentPage"
    page_size_query_param = "showCount"

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)
        self.page_number = page_number
        self.num_pages = paginator.num_pages
        self.page_size = page_size

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):

        return Response(OrderedDict([
            ('code', 0),
            ('msg', 'success'),
            ('data',OrderedDict([
                    ('currentPage', self.page_number),
                    ('showCount', self.page_size),
                    ('totalResult',self.page.paginator.count),
                    ('totalPage', self.num_pages),
                    ('dataList', data)
            ])),
        ]))
