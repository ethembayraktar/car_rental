import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from utils import factories

"""
This router includes routes for the standard set of list, create, retrieve, update, partial_update and destroy actions. 

URL Style	                    HTTP          Method Action	                              URL Name
============================================================================================================
{prefix}/	                    GET	          list	                                     {basename}-list
                                POST	      create

{prefix}/{url_path}/	        GET,*	      `@action(detail=False)`,**                  m{basename}-{url_name}
{prefix}/{lookup}/	            GET	           retrieve	                                  {basename}-detail
                                PUT	           update
                                PATCH	       partial_update
                                DELETE	       destroy
{prefix}/{lookup}/{url_path}/	GET,*	`@action(detail=True)` decorated method	          {basename}-{url_name}


*   or as specified by `methods` argument
**  decorated method
"""

# class GetAllCountryTest(TestCase):
#     """ Test module for GET all countrys API """
#
#     def setUp(self):
#         self.logo = Attachment.objects.filter(slug__icontains="ziraat").first()
#         Country.objects.create(name='Ziraat Countryası', url='https://www.ziraatcountry.com.tr/', logo=self.logo)
#         Country.objects.create(name='Garanti Countryası', url='https://www.garantibbva.com.tr/', logo=self.logo)
#         Country.objects.create(name='Akcountry Countryası', url='https://www.akcountry.com/', logo=self.logo)
#
#     def test_get_all_countrys(self):
#         """
#         We use CustomePagination, so return seralized data in response.data["data"]
#         """
#         response = client.get(reverse('country-list'))
#         # get data from db
#         countrys = Country.objects.all()
#         serializer = CountrySerializer(countrys, many=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["data"], serializer.data)
#
#
# class GetSingleCountryTest(TestCase):
#     """ Test module for GET single country API """
#
#     def setUp(self):
#         self.logo = Attachment.objects.filter(slug__icontains="ziraat").first()
#         self.country = Country.objects.create(name='Ziraat Countryası', url='https://www.ziraatcountry.com.tr/',
#                                               logo=self.logo)
#         self.country2 = Country.objects.create(name='Garanti Countryası', url='https://www.garantibbva.com.tr/',
#                                                logo=self.logo)
#         self.country3 = Country.objects.create(name='Akcountry Countryası', url='https://www.akcountry.com/',
#                                                logo=self.logo)
#
#     def test_get_valid_single_country(self):
#         response = client.get(reverse('country-detail', kwargs={'pk': self.country2.pk}))
#         country = Country.objects.get(pk=self.country2.pk)
#         serializer = CountrySerializer(country)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_invalid_country_country(self):
#         response = client.get(reverse('country-detail', kwargs={'pk': 900}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# class CreateNewCountryTest(TestCase):
#     """
#     Test module for inserting a new country
#     """
#     client_admin = APIClient()
#     user = User.objects.get(email="admin@guvenassist.com")
#     client_admin.force_authenticate(user=user)
#
#     def setUp(self):
#         self.valid_payload = {
#             "name": "Ziraat Countryası",
#             "url": "https://www.ziraatcountry.com.tr/",
#         }
#
#         self.invalid_payload = {
#             "email": "https://www.ziraatcountry.com.tr/",
#             "score": 2,
#         }
#
#     def test_create_invalid_country_no_authentication(self):
#         response = client.post(
#             reverse('country-list'),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_create_valid_country(self):
#         response = self.client_admin.post(reverse('country-list'),
#                                           data=json.dumps(self.valid_payload),
#                                           content_type='application/json'
#                                           )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_create_invalid_country(self):
#         response = self.client_admin.post(
#             reverse('country-list'),
#             data=json.dumps(self.invalid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class UpdateSingleCountryTest(TestCase):
#     """
#     Test module for updating an existing country record
#     """
#     client_admin = APIClient()
#     user = User.objects.get(email="admin@guvenassist.com")
#     client_admin.force_authenticate(user=user)
#
#     def setUp(self):
#         self.logo = Attachment.objects.filter(slug__icontains="ziraat-countryasi").first()
#         self.logo2 = Attachment.objects.filter(slug__icontains="garanti-bbva").first()
#
#         self.country = Country.objects.create(name='Ziraat Countryası', url='https://www.ziraatcountry.com.tr/',
#                                               logo=self.logo)
#         self.country2 = Country.objects.create(name='Garanti BBVA', url='https://www.garantibbva.com.tr/',
#                                                logo=self.logo2)
#
#         self.valid_payload = {
#             'name': 'Ziraat Countryası Updated',
#             'url': 'https://www.ziraatcountry.com.tr/',
#         }
#         self.invalid_payload = {
#             'url': 'https://www.ziraatcountry.com.tr/',
#         }
#
#     def test_valid_update_country(self):
#         response = self.client_admin.put(
#             reverse('country-detail', kwargs={'pk': self.country2.pk}),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# class DeleteSingleCountryTest(TestCase):
#     """
#     Test module for deleting an existing country record
#     """
#     client_admin = APIClient()
#     client_customer = APIClient()
#
#     def setUp(self):
#         self.logo = Attachment.objects.filter(slug__icontains="ziraat-countryasi").first()
#         self.logo2 = Attachment.objects.filter(slug__icontains="garanti-countryasi").first()
#         self.country = Country.objects.create(name='Ziraat Countryası', url='https://www.ziraatcountry.com.tr/',
#                                               logo=self.logo)
#         self.country2 = Country.objects.create(name='Garanti Countryası', url='https://www.garantibbva.com.tr/',
#                                                logo=self.logo2)
#
#         admin_user, created = User.objects.get_or_create(email="admin@guvenassist.com",
#                                                          is_superuser=True,
#                                                          is_staff=True)
#         customer_user, created = User.objects.get_or_create(email="customer@guvenassist.com")
#         self.client_admin.force_authenticate(user=admin_user)
#
#         self.client_customer.force_authenticate(user=customer_user)
#
#     def test_valid_delete_country(self):
#         response = self.client_admin.delete(reverse('country-detail', kwargs={'pk': self.country.pk}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#         response = self.client_customer.delete(reverse('country-detail', kwargs={'pk': self.country2.pk}))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         response = self.client_admin.delete(reverse('country-detail', kwargs={'pk': self.country2.pk}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#     def test_invalid_delete_country(self):
#         response = self.client_admin.delete(reverse('country-detail', kwargs={'pk': 30}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# class DeleteManyCountryTest(TestCase):
#     """
#     Test module for deleting an existing country record
#     """
#     client_admin = APIClient()
#     client_customer = APIClient()
#
#     def setUp(self):
#         self.logo = Attachment.objects.filter(slug__icontains="ziraat-countryasi").first()
#         self.logo2 = Attachment.objects.filter(slug__icontains="garanti-countryasi").first()
#         self.country = Country.objects.create(name='Ziraat Countryası', url='https://www.ziraatcountry.com.tr/',
#                                               logo=self.logo)
#         self.country2 = Country.objects.create(name='Garanti Countryası', url='https://www.garantibbva.com.tr/',
#                                                logo=self.logo2)
#
#         admin_user, created = User.objects.get_or_create(email="admin@guvenassist.com",
#                                                          is_superuser=True,
#                                                          is_staff=True)
#         customer_user, created = User.objects.get_or_create(email="customer@guvenassist.com")
#         self.client_admin.force_authenticate(user=admin_user)
#
#         self.client_customer.force_authenticate(user=customer_user)
#
#     def test_valid_delete_country(self):
#         payload = {'items': [self.country.pk, self.country2.pk]}
#         response = self.client_admin.delete(reverse('country-delete_many'),
#                                             data=json.dumps(payload),
#                                             content_type='application/json'
#                                             )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
