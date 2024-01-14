import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from country.models import Ilce
from country.serializers import IlceSerializer
from utils import factories
from utils.factories import IlceFactory


class TestIlceAPIViewSet(APITestCase):
    def setUp(self):
        self.ilce = IlceFactory()
        self.ilce2 = IlceFactory()
        self.superuser = factories.SuperUserFactory()
        self.client.force_authenticate(user=self.superuser)

    def test_get_detail(self):
        response = self.client.get(reverse('ilce-detail', kwargs={'pk': self.ilce.pk}))
        self.assertEquals(200, response.status_code)
        serializer = IlceSerializer(self.ilce)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_get_list(self):
        response = self.client.get(reverse('ilce-list') + "?ordering=-id")
        self.assertEquals(200, response.status_code)

        all_ilce = Ilce.objects.filter(is_deleted=False).order_by("-id")
        serializer = IlceSerializer(all_ilce, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(serializer.data, response.data["data"])

    def test_put(self):
        data = json.dumps({"name": "Wonderland"}),
        content_type = 'application/json'
        existing_ilce_name = self.ilce.name
        response = self.client.put(reverse('ilce-detail', kwargs={'pk': self.ilce.pk}),
                                   data=data,
                                   content_type='application/json')

        self.assertEquals(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        self.assertEqual(self.ilce.name, existing_ilce_name)

    def test_delete(self):
        existing_il_name = self.ilce2.name
        response = self.client.delete(reverse('ilce-detail', kwargs={'pk': self.ilce2.pk}))

        self.assertEquals(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        self.assertEqual(self.ilce2.name, existing_il_name)
