from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import viewsets, parsers, filters
from rest_framework.response import Response

from country.filters import IlFilter, IlceFilter, MahalleKoyFilter, SokakFilter, CarMarkFilter, CarModelFilter, \
    VehicleTypeFilter
from country.models import Il, Ilce, MahalleKoy, Sokak, CarModel, CarMark, VehicleType
from country.serializers import MahalleKoySerializer, IlSerializer, IlceSerializer, SokakSerializer, CarModelSerializer, \
    CarMarkSerializer, VehicleTypeSerializer
from utils.pagination import LargeResultsSetPagination, VeryLargeResultsSetPagination
from utils.parsers import MultipartJsonParser
from utils.permissions import IsSuperuser, PermissionPolicyMixin
from utils.util import MyModelViewSet


class IlViewSet(PermissionPolicyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Il.objects.filter(is_active=True, is_deleted=False)
    serializer_class = IlSerializer
    pagination_class = LargeResultsSetPagination
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = IlFilter
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    CACHE_KEY_PREFIX = "il-view"
    ordering_fields = ['id', 'name']
    search_fields = ['id', 'name']
    lookup_field = 'pk'

    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "list": [],
        "retrieve": [],
        "create": [IsSuperuser],
        "update": [IsSuperuser],
        "partial_update": [IsSuperuser],
        "destroy": [IsSuperuser],
    }

    def list(self, request, *args, **kwargs):
        model_name = self.get_serializer_class().Meta.model.__name__
        absolute_url = request.build_absolute_uri()
        hashed_absolute_url = hash(absolute_url)
        data = cache.get(f"{model_name}_{hashed_absolute_url}")
        if data:
            return Response(data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serialized_data = serializer.data
            response = self.get_paginated_response(serialized_data)
            cache.set(f"{model_name}_{hashed_absolute_url}", response.data)
            return response

        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data
        data = cache.set(f"{model_name}_{hashed_absolute_url}", serialized_data)
        return Response(serialized_data)


class IlceViewSet(PermissionPolicyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Ilce.objects.filter(is_active=True, is_deleted=False)
    serializer_class = IlceSerializer
    pagination_class = LargeResultsSetPagination
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = IlceFilter
    CACHE_KEY_PREFIX = "ilce-view"
    ordering_fields = ['id', 'name']
    search_fields = ['id', 'name']
    lookup_field = 'pk'

    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "list": [],
        "retrieve": [],
        "create": [IsSuperuser],
        "update": [IsSuperuser],
        "partial_update": [IsSuperuser],
        "destroy": [IsSuperuser],
    }

    def list(self, request, *args, **kwargs):
        model_name = self.get_serializer_class().Meta.model.__name__
        absolute_url = request.build_absolute_uri()
        hashed_absolute_url = hash(absolute_url)
        data = cache.get(f"{model_name}_{hashed_absolute_url}")
        if data:
            return Response(data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serialized_data = serializer.data
            response = self.get_paginated_response(serialized_data)
            cache.set(f"{model_name}_{hashed_absolute_url}", response.data)
            return response

        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data
        data = cache.set(f"{model_name}_{hashed_absolute_url}", serialized_data)
        return Response(serialized_data)


class MahalleKoyViewSet(PermissionPolicyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = MahalleKoy.objects.filter(is_active=True, is_deleted=False)
    serializer_class = MahalleKoySerializer
    pagination_class = LargeResultsSetPagination
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MahalleKoyFilter
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    CACHE_KEY_PREFIX = "mahallekoy-view"
    ordering_fields = ['id', 'name']
    search_fields = ['id', 'name', 'ilce__name', 'ilce__il__name']
    lookup_field = 'pk'

    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "list": [],
        "retrieve": [],
        "create": [IsSuperuser],
        "update": [IsSuperuser],
        "partial_update": [IsSuperuser],
        "destroy": [IsSuperuser],
    }

    def list(self, request, *args, **kwargs):
        model_name = self.get_serializer_class().Meta.model.__name__
        absolute_url = request.build_absolute_uri()
        hashed_absolute_url = hash(absolute_url)
        data = cache.get(f"{model_name}_{hashed_absolute_url}")
        if data:
            return Response(data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serialized_data = serializer.data
            response = self.get_paginated_response(serialized_data)
            cache.set(f"{model_name}_{hashed_absolute_url}", response.data)
            return response

        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data
        data = cache.set(f"{model_name}_{hashed_absolute_url}", serialized_data)
        return Response(serialized_data)


class SokakViewSet(PermissionPolicyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Sokak.objects.filter(is_active=True, is_deleted=False)
    serializer_class = SokakSerializer
    pagination_class = LargeResultsSetPagination
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = SokakFilter
    CACHE_KEY_PREFIX = "sokak-view"
    ordering_fields = ['id', 'name']
    search_fields = ['id', 'name']
    lookup_field = 'pk'

    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "list": [],
        "retrieve": [],
        "create": [IsSuperuser],
        "update": [IsSuperuser],
        "partial_update": [IsSuperuser],
        "destroy": [IsSuperuser],
    }

    def list(self, request, *args, **kwargs):
        model_name = self.get_serializer_class().Meta.model.__name__
        absolute_url = request.build_absolute_uri()
        hashed_absolute_url = hash(absolute_url)
        data = cache.get(f"{model_name}_{hashed_absolute_url}")
        if data:
            return Response(data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serialized_data = serializer.data
            response = self.get_paginated_response(serialized_data)
            cache.set(f"{model_name}_{hashed_absolute_url}", response.data)
            return response

        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data
        data = cache.set(f"{model_name}_{hashed_absolute_url}", serialized_data)
        return Response(serialized_data)


class CarMarkViewSet(MyModelViewSet):
    queryset = CarMark.objects.filter(is_active=True, is_deleted=False).order_by("name")
    serializer_class = CarMarkSerializer
    pagination_class = VeryLargeResultsSetPagination
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CarMarkFilter
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    CACHE_KEY_PREFIX = "carmark-view"
    ordering_fields = ['id', 'name']
    search_fields = ['id', 'name']
    lookup_field = 'pk'

    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "list": [],
        "retrieve": [],
        "create": [IsSuperuser],
        "update": [IsSuperuser],
        "partial_update": [IsSuperuser],
        "destroy": [IsSuperuser],
    }


class CarModelViewSet(MyModelViewSet):
    queryset = CarModel.objects.filter(is_active=True, is_deleted=False).order_by('name')
    serializer_class = CarModelSerializer
    pagination_class = VeryLargeResultsSetPagination
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CarModelFilter
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    CACHE_KEY_PREFIX = "carmodel-view"
    ordering_fields = ['id', 'name']
    search_fields = ['id', 'name']
    lookup_field = 'pk'

    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "list": [],
        "retrieve": [],
        "create": [IsSuperuser],
        "update": [IsSuperuser],
        "partial_update": [IsSuperuser],
        "destroy": [IsSuperuser],
    }


class VehicleTypeViewSet(PermissionPolicyMixin, viewsets.ReadOnlyModelViewSet):
    queryset = VehicleType.objects.filter(is_active=True, is_deleted=False)
    serializer_class = VehicleTypeSerializer
    pagination_class = LargeResultsSetPagination
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = VehicleTypeFilter
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    ordering_fields = ['id', 'name']
    search_fields = ['id', 'name']
    lookup_field = 'pk'

    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "list": [],
        "retrieve": [],
        "create": [IsSuperuser],
        "update": [IsSuperuser],
        "partial_update": [IsSuperuser],
        "destroy": [IsSuperuser],
    }
