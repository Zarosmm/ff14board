from collections import OrderedDict

from django.core.paginator import InvalidPage
from rest_framework import pagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class PagePagination(pagination.PageNumberPagination):

    page_size = 10
    page_query_param = "currentPage"
    page_size_query_param = "showCount"
    sort_field_param = "sortField"  # 前端传入的排序字段参数名
    sort_order_param = "sortOrder"  # 前端传入的排序顺序参数名（asc/desc）

    def paginate_queryset(self, queryset, request, view=None):
        """
        分页 queryset，如果需要，返回页面对象；如果未配置分页，返回 None。
        """
        # 获取排序参数
        sort_field = request.query_params.get(self.sort_field_param, 'id')  # 默认排序字段为 'id'
        sort_order = request.query_params.get(self.sort_order_param, 'asc')  # 默认升序

        # 验证排序字段（可选：防止 SQL 注入）
        allowed_fields = ['id', 'created_at']  # 可排序的字段列表，根据 Team 模型调整
        if sort_field not in allowed_fields:
            sort_field = 'id'  # 无效字段时使用默认字段

        # 应用排序
        if sort_order.lower() == 'desc':
            sort_field = f'-{sort_field}'  # 降序加前缀 '-'
        queryset = queryset.order_by(sort_field)

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
