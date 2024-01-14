from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param


class NotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'bad_request.'
    default_code = 'bad_request'


class CustomPagination(PageNumberPagination):
    page_size = 10
    page = 1
    max_page_size = 1000000
    page_size_query_param = 'limit'
    page_query_param = 'page'
    request = None

    def get_current_link(self):
        url = self.request.build_absolute_uri()
        return replace_query_param(url, self.page_query_param, self.page.number)

    def get_first_link(self):
        if self.page.paginator.num_pages == 0:
            return None
        url = self.request.build_absolute_uri()
        page_number = 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_last_link(self):
        if self.page.paginator.num_pages <= 1:
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self.page_size = self.get_page_size(request)
        if not self.page_size:
            return None

        paginator = self.django_paginator_class(queryset, self.page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except Exception as exc:
            # Here it is
            msg = {
                "code": 400,
                "error": "Page out of range"
            }
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        """
          current_page: number;
          data: T[];
          first_page_url: string;
          from: number;
          last_page: number;
          last_page_url: string;
          links: any[];
          next_page_url: string | null;
          path: string;
          per_page: number;
          prev_page_url: string | null;
          to: number;
          total: number;

        """
        return Response({
            'next_page_url': self.get_next_link(),
            'prev_page_url': self.get_previous_link(),
            "first_page_url": self.get_first_link(),
            "last_page_url": self.get_last_link(),
            "data": data,
            "total": self.page.paginator.count,
            "currentPage": int(self.request.query_params.get('page', 1)),
            "current_page": int(self.request.query_params.get('page', 1)),
            "last_page": self.page.paginator.num_pages,
            "lastPage": self.page.paginator.num_pages,
            "firstItem": self.page.start_index(),
            "lastItem": self.page.end_index(),
            "perPage": self.page_size,
            "per_page": self.page_size,
            "to": self.page.start_index(),
            "from": self.page.end_index(),
            "recordsTotal": self.page.paginator.count,
            "recordsFiltered": self.page.paginator.count,
        }
        )


class HugeLargeResultsSetPagination(CustomPagination):
    page_size = 100000
    max_page_size = 1000000


class VeryLargeResultsSetPagination(CustomPagination):
    page_size = 10000
    max_page_size = 100000


class LargeResultsSetPagination(CustomPagination):
    page_size = 1000
    max_page_size = 10000


class StandardResultsSetPagination(CustomPagination):
    page_size = 100
    max_page_size = 1000


class BlogPostPagination(CustomPagination):
    page_size = 9
    max_page_size = 100