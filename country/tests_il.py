import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from country.models import Il
from country.serializers import IlSerializer
from utils import factories
from utils.factories import IlFactory


class TestIlAPIViewSet(APITestCase):
    def setUp(self):
        self.il = IlFactory()
        self.il2 = IlFactory()
        self.superuser = factories.SuperUserFactory()
        self.client.force_authenticate(user=self.superuser)

    def test_get_detail(self):
        response = self.client.get(reverse('il-detail', kwargs={'pk': self.il.pk}))
        self.assertEquals(200, response.status_code)
        serializer = IlSerializer(self.il)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_get_list(self):
        response = self.client.get(reverse('il-list') + "?ordering=-id")
        self.assertEquals(200, response.status_code)

        all_ils = Il.objects.filter(is_deleted=False).order_by("-id")
        serializer = IlSerializer(all_ils, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(serializer.data, response.data["data"])

    def test_put(self):
        data = json.dumps({"name": "Wonderland"}),
        content_type = 'application/json'
        existing_il_name = self.il.name
        response = self.client.put(reverse('il-detail', kwargs={'pk': self.il.pk}),
                                   data=data,
                                   content_type='application/json')

        self.assertEquals(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        self.assertEqual(self.il.name, existing_il_name)

    def test_delete(self):
        existing_il_name = self.il2.name
        response = self.client.delete(reverse('il-detail', kwargs={'pk': self.il2.pk}))

        self.assertEquals(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        self.assertEqual(self.il2.name, existing_il_name)
