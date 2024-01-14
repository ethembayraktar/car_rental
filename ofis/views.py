import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import parsers, filters

from attachment.serializers import AttachmentSerializer
from ofis.filters import OfisFilter
from ofis.models import Ofis
from ofis.serializers import OfisSerializer
from user.serializers import UserPublicSerializer
from utils.pagination import LargeResultsSetPagination
from utils.parsers import MultipartJsonParser
from utils.permissions import IsSuperuser, IsCallCenter
from utils.util import MyModelViewSet


class OfisView(LoginRequiredMixin, View):
    def get(self, request, code=None):
        context = {
            'menu_open': [],
            'active': ["#ofiss_li"],
        }
        if code:
            context["ofis"] = Ofis.objects.filter(code=code).first()
            template = loader.get_template('assist/super_admin/ofis_private.html')
        else:
            template = loader.get_template('assist/super_admin/ofiss_all.html')
        return HttpResponse(template.render(context, request))


class OfisDatatableView(LoginRequiredMixin, BaseDatatableView):
    def get_initial_queryset(self):
        self.max_display_length = 20
        self.model = Ofis

        self.columns = ["logo",
                        "name",
                        "code",
                        "referans",
                        "first_name",
                        "last_name",
                        "vkn",
                        "bank",
                        "iban",
                        "phone",
                        "email",
                        "il",
                        "ilce",
                        "address",
                        "bank",
                        "iban",
                        ]

        self.order_columns = ["logo",
                              "name",
                              "code",
                              "referans",
                              "first_name",
                              "last_name",
                              "vkn",
                              "bank",
                              "iban",
                              "phone",
                              "email",
                              "il",
                              "ilce",
                              "address",
                              "bank",
                              "iban",
                              ]
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.none()

    def filter_queryset(self, qs):
        try:
            my_search = self.request.GET.get('search[value]', None)
            if my_search and not my_search == "":
                q = (Q(id__icontains=my_search) |
                     Q(code__icontains=my_search) |
                     Q(reference_code__icontains=my_search) |
                     Q(first_name__icontains=my_search) |
                     Q(last_name__icontains=my_search) |
                     Q(email__icontains=my_search) |
                     Q(username__icontains=my_search)
                     )
                qs = qs.filter(q)
            return qs
        except Exception as e:
            logging.exception(e)
            return qs

    def prepare_results(self, qs):
        json_data = []
        i = 1

        for item in qs:
            json_data.append({
                "id": item.id,
                "pk": item.pk,
                "user": UserPublicSerializer(item.user).data if item.user else None,
                "logo": AttachmentSerializer(item.logo).data if item.logo else None,
                "code": item.code,
                "reference_code": item.reference_code,
                "name": item.name,
                "email": item.email,
                "vkn": item.email,
                "phone": item.phone,
                "bank": item.bank,
                "iban": item.iban,
                "il": item.il.name if item.il else None,
                "ilce": item.ilce.name if item.ilce else None,
                "address": item.address,
                "created_at": item.created_at.strftime("%Y-%m-%d  %H:%M:%S"),
                "is_active": item.is_active,
                "is_deleted": item.is_deleted
            })
            i += 1
        return json_data


class OfisViewSet(MyModelViewSet):
    queryset = Ofis.objects.filter(is_active=True, is_deleted=False)
    serializer_class = OfisSerializer
    pagination_class = LargeResultsSetPagination
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = OfisFilter
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    CACHE_KEY_PREFIX = "il-view"
    ordering_fields = ['id', 'name']
    search_fields = ['id', 'name']
    lookup_field = 'pk'

    permission_classes_per_method = {
        "list": [IsSuperuser | IsCallCenter],
        "retrieve": [IsSuperuser | IsCallCenter],
        "create": [IsSuperuser | IsCallCenter],
        "update": [IsSuperuser | IsCallCenter],
        "partial_update": [IsSuperuser | IsCallCenter],
        "destroy": [IsSuperuser | IsCallCenter],
    }
