import base64
import io
import json
import logging
import os
import random
from datetime import datetime
from random import randint
from urllib.request import Request, urlopen
from uuid import UUID

import requests
from PIL import Image
from cryptography.fernet import Fernet
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.timezone import make_aware
from dotenv import load_dotenv
from drf_yasg.renderers import OpenAPIRenderer, SwaggerUIRenderer
from lxml import etree
from rest_framework import parsers
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from core.settings import GOOGLE_RECAPTCHA_SECRET_KEY, ENCRYPT_KEY, BASE_DIR
from utils.atomic_viewsets import AtomicModelViewSet
from utils.garanti import sha512, sha1
from utils.pagination import StandardResultsSetPagination
from utils.parsers import MultipartJsonParser
from utils.permissions import PermissionPolicyMixin

load_dotenv()

logger = logging.getLogger("default")

os.environ["TZ"] = "UTC"

naive_datetime = datetime.now()
aware_datetime = make_aware(naive_datetime)

CONTENT_TYPES = ['image', 'video']
MAX_UPLOAD_SIZE = "20971520"

extension_dict = {
    'pdf': "pdf.png",
    'doc': "word.png",
    'docx': "word.png",
    'xlsx': "excel.png",
    'mp3': "mp3.png",
    'wav': "wav.png",
    'mp4': "mp4.png",
    "video": "video.png",
    "audio": "audio.png"
}

IYZICO_OPTIONS = {
    'api_key': os.getenv("IYZICO_APIKEY"),
    'secret_key': os.getenv("IYZICO_SECRET_KEY"),
    'base_url': os.getenv("IYZICO_BASE_URL"),
}
IYZICO_OPTIONS_SANDBOX = {
    'api_key': os.getenv("IYZICO_APIKEY_SANDBOX"),
    'secret_key': os.getenv("IYZICO_SECRET_KEY_SANDBOX"),
    'base_url': os.getenv("IYZICO_BASE_URL_SANDBOX"),
}


class EnablePartialUpdateMixin:
    """
    Enable partial updates
    """

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


class MyModelViewSet(PermissionPolicyMixin, EnablePartialUpdateMixin, AtomicModelViewSet):
    paginate_by_param = 'limit'
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    pagination_class = StandardResultsSetPagination
    authentication_classes = [TokenAuthentication, BasicAuthentication, SessionAuthentication, JWTAuthentication]
    permission_classes = []
    lookup_field = 'pk'
    ordering = ['-id']
    cached_models = ["CarMark", "CarModel", "Il", "Ilce"]
    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "list": [],
        "retrieve": [],
        "create": [],
        "update": [],
        "partial_update": [],
        "destroy": [],
    }

    def retrieve(self, request, *args, **kwargs):
        model = self.serializer_class.Meta.model
        model_name = model.__name__
        model_pk_type = model.get_pk_type()

        if model_name in self.cached_models:
            cached_data = self.get_cached_data(request)
            if cached_data:
                return Response(cached_data)

        if kwargs['pk'] == "undefined":
            return Response()
        if (model_pk_type in ['AutoField', 'BigAutoField'] and (isinstance(kwargs['pk'], int) or
                                                                (isinstance(kwargs['pk'], str) and
                                                                 kwargs['pk'].isnumeric())) and
                self.queryset.filter(pk=kwargs['pk']).exists()):
            instance = self.queryset.filter(pk=kwargs['pk']).first()
        elif (model_pk_type == 'UUIDField' and is_valid_uuid(kwargs['pk']) and
              self.queryset.filter(pk=kwargs['pk']).exists()):
            instance = self.queryset.filter(pk=kwargs['pk']).first()
        else:
            instance = self.queryset.filter(slug=kwargs['pk']).first()

        if instance:
            if hasattr(instance, "hit"):
                instance.hit += 1
                instance.save()
            serializer = self.get_serializer(instance, context=self.get_serializer_context())
            return Response(serializer.data)
        return Response()

    def list(self, request, *args, **kwargs):
        model_name = self.get_serializer_class().Meta.model.__name__
        if model_name in self.cached_models:
            cached_data = self.get_cached_data(request)
            if cached_data:
                return Response(cached_data)

        absolute_url = request.build_absolute_uri()
        hashed_absolute_url = hash(absolute_url)

        queryset = self.filter_queryset(self.get_queryset())
        # print(queryset.query)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serialized_data = serializer.data
            response = self.get_paginated_response(serialized_data)

            if model_name in self.cached_models:
                data = cache.set(f"{model_name}_{hashed_absolute_url}", response.data)

            return response

        serializer = self.get_serializer(queryset, many=True)
        serialized_data = serializer.data

        if model_name in self.cached_models:
            data = cache.set(f"{model_name}_{hashed_absolute_url}", serialized_data)

        return Response(serialized_data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        language = self.request.GET.get('language', None)
        if language is None and "HTTP_ACCEPT_LANGUAGE" in self.request.META:
            if self.request.META["HTTP_ACCEPT_LANGUAGE"] == "en":
                language = "en"
            else:
                language = "tr"

        if language:
            context = super().get_serializer_context()
            context.update({"language": language})
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"status": "success",
                         "message": "Instance is deleted"},
                        status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.is_active = False
        instance.deleted_at = timezone.now()

        instance.deleted_by = self.request.user
        instance.save()

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_cached_data(self, request):
        model_name = self.get_serializer_class().Meta.model.__name__
        absolute_url = request.build_absolute_uri()
        hashed_absolute_url = hash(absolute_url)
        data = None
        self.queryset = self.get_queryset()

        if model_name in self.cached_models:
            data = cache.get(f"{model_name}_{hashed_absolute_url}")
            if data:
                return data

        return None


def remove_html_tags(text):
    parser = etree.HTMLParser()
    tree = etree.fromstring(text, parser)
    return etree.tostring(tree, encoding='unicode', method='text')


def load_file_from_url(url):
    # file = urlopen(url).read()
    # return load_workbook(filename=BytesIO(file))

    req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    file = urlopen(req).read()
    return io.BytesIO(file)


def clear_string(my_string: str):
    if my_string:
        my_string = my_string.replace("_x000D_\n", "").replace("_x000d_\n", "").replace("\r", "").replace(
            "_x000D\n", "").replace("_x000d\n", ""). \
            replace("_x000D", "").replace("_x000d", "").strip()

    return my_string


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    permissions = []
    for g in user.groups.all():
        permissions.append(g.name)
    return {"token": refresh.access_token,
            "permissions": permissions
            }


def clear_temp_files(files):
    """
    Delete temp file from media root
    """

    temp_files_set = set(files)

    for temp_file in temp_files_set:
        try:
            temp_path = os.path.join(settings.MEDIA_ROOT, "temp", temp_file)
            os.remove(temp_path)
        except Exception as e:
            print(f"Error in deleting temp file = {e}")


def delete_cache(key_prefix: str):
    """
    Delete all cache keys with the given prefix.
    """

    keys_pattern = f"views.decorators.cache.cache_*.{key_prefix}.*.{settings.LANGUAGE_CODE}.{settings.TIME_ZONE}"
    cache.delete_pattern(keys_pattern)


def validate_recaptche(recaptcha_response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    response = requests.post(url, data=values)
    result = response.json()
    return result['success']


def make_transparent(file):
    from core.settings import MEDIA_ROOT
    img = Image.open(file)
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(os.path.join(MEDIA_ROOT, "profiles", "avatar", "file2"), "PNG")


def get_client_ip(request):
    if request is None:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_device(request):
    return request.META['HTTP_USER_AGENT']


def get_next_id(model_class):
    items = model_class.objects.all().order_by('-id')
    if items.count() == 0:
        return 1
    return items[0].id + 1


default_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'


def get_random_string(length, allowed_chars=default_chars):
    random_string = ""
    for i in range(length):
        random_string += random.choice(allowed_chars)
    return random_string


def get_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return get_random_string(50, chars)


def two_weeks_hence():
    return timezone.now() + timezone.timedelta(days=14)


def one_month_hence():
    return timezone.now() + timezone.timedelta(days=30)


def one_year_hence():
    return timezone.now() + timezone.timedelta(days=365)


def ten_years_hence():
    return timezone.now() + timezone.timedelta(days=3650)


def random_with_n_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def xml_escape(string):
    string = string.replace('&lt;![CDATA[', '')
    string = string.replace(']]&gt;', '')
    string = string.replace('&', '&amp;')
    return string


def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return None
    for x in a:
        if not x.isdigit():
            return None
        i = int(x)
        if i < 0 or i > 255:
            return None
    return s


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.xlsx', '.xls', '.ico', '.webp', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def hash_data(order_id, amount, password, terminalId, storeKey, successurl, errorurl):
    """
    Bu doküman içerisinde, birçok işlem tipi altında kullanılan ve istek mesajı içerisinde <HashData> şeklinde yer
    alan etiket için gerekli olan verinin nasıl oluşturulacağını adım adım anlatılmaktadır.
    İstek mesajları içerisinde yer alan <HashData> etiketi; kullanıcıya ait şifre doğrulamasının yapılmasını
    sağlayan alandır. Hash oluşturma detayları aşağıda ayrıca anlatılmaktadır.

    Yeni SanalPoS uygulamasında, terminale ait şifrenin açık şekilde dolaşmasının engellenmesi için HASH
    yapısı kullanılmaktadır.

    Hash hesabı:
    Hashedpassword bilgisinin hesaplanmasında SHA1
    Hashvalue değerinin hesaplanmasında SHA512 algoritması kullanılmaktadır.
    Hash hesaplamasında, İki parçalı HASH yapısı kullanılmaktadır. İlk aşamada provizyon şifresinin,
    terminal numarası ile yanyana getirilmesi ile SHA1 algoritması kullanılarak hashedpassword değerinin elde
    edilmesi sağlanacaktır.

    Hash oluşturmak için gerekli olan işlemler, aşağıda farklı programlama dilleri için sunulmuştur:

    terminalId . $orderId . $amount . $currencyCode . $successUrl . $errorUrl . $type. $storeKey . $hashedPassword)
    MerchantID	7000679
    ProvUserID	PROVAUT / PROVRFN / PROVOOS
    ProvisionPassword	123qweASD/
    TerminalID	30691297
    StoreKey	12345678
    """

    data = f"{password}{terminalId.zfill(9)}"
    print(data)

    hashedPassword = sha1(data)

    print("hashedPassword= " + hashedPassword)

    hashedDataStr = f"{terminalId}{order_id}{amount}{949}{successurl}{errorurl}{'sales'}{storeKey}{hashedPassword}"
    hashedData = sha512(hashedDataStr)
    print("hashedDataStr = " + hashedDataStr)
    print("hashedData = " + hashedData)
    return hashedData


def encrypt(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        cipher_suite = Fernet(bytes(ENCRYPT_KEY, 'utf-8'))  # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii")
        return encrypted_text
    except Exception as e:
        # log the error if any
        logging.exception(e)
        return None


def decrypt(txt):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")
        return decoded_text
    except Exception as e:
        # log the error
        logging.exception(e)
        return None


def send_comment_notification(user_ids, my_dict):
    from channels.layers import get_channel_layer
    from notification.models import Notification, NotificationUserRelation
    from asgiref.sync import async_to_sync
    from user.models import User
    try:
        my_bildirim = Notification.objects.create(title=my_dict["title"],
                                                  text=my_dict["body"])

        for user_id in user_ids:
            channel_layer = get_channel_layer()
            my_relation = NotificationUserRelation.objects.create(notification=my_bildirim,
                                                                  user=User.objects.filter(id=user_id).first()
                                                                  )

            group_name = f'user_{user_id}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {'type': 'user_message',
                 'data': {'title': my_bildirim.title,
                          'mesaj': my_bildirim.text
                          }
                 }
            )
    except Exception as e:
        logging.exception(f"Error in send_admin_notification {e}")


def send_admin_notification(my_dict):
    from channels.layers import get_channel_layer
    from notification.models import Notification, NotificationUserRelation
    from asgiref.sync import async_to_sync
    from user.models import User
    try:
        if "title" not in my_dict:
            my_dict["title"] = "<p class='text'>Yeni Admin Bildirim</p>"

        if "text" not in my_dict:
            my_dict["text"] = "<p class='text'>Yeni Admin Bildirimi oluşturuldu</p>"

        if "icon'" not in my_dict:
            my_dict["icon"] = "<i class='icon-info text-warning'></i>"

        my_bildirim = Notification.objects.create(title=my_dict["title"],
                                                  text=my_dict["text"],
                                                  icon=my_dict["icon"]
                                                  )

        for super_user in User.objects.filter(is_active=True, is_deleted=False, is_superuser=True):
            channel_layer = get_channel_layer()
            my_relation = NotificationUserRelation.objects.create(notification=my_bildirim,
                                                                  user=super_user
                                                                  )

            group_name = f'user_{super_user.id}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {'type': 'user_message',
                 'data': {'title': my_dict["title"],
                          'text': my_dict["text"],
                          'icon': my_dict["icon"],
                          'created_at': my_bildirim.created_at.strftime("%Y-%m-%d  %H:%M:%S")
                          }
                 }
            )
    except Exception as e:
        logging.exception(f"Error in send_admin_notification {e}")


def parse_car_brands():
    from customer.models import CarModel, CarMark
    with io.open(os.path.join(BASE_DIR, "utils", "data", "car_brands.json"), encoding="utf-8") as json_file:
        data_dict = json.load(json_file)
        car_brands = data_dict["items"]
        """
        [{"code":"003",
        "name":"ALFA ROMEO",
        "carModels":[
        {"brandId":1,
        "typeCode":"055",
        "name":"1600 SW",
        "id":54150},
        {"brandId":1,"typeCode":"1005","name":"4C LAUNCH EDITION 1.750 TB 240 TCT ","id":8},{"brandId":1,"typeCode":"1006","name":"159 2.4 DIZEL SPORTSWAGON ","id":9},
        """
        for car_brand in car_brands:
            car_brand_name = car_brand["name"]
            car_brand_code = car_brand["code"]
            # print(car_brand_name)
            # print(car_brand_code)
            if CarMark.objects.filter(name=car_brand_name, code=car_brand_code).exists():
                car_mark = CarMark.objects.filter(name=car_brand_name, code=car_brand_code).first()
            else:
                car_mark = CarMark.objects.create(name=car_brand_name, code=car_brand_code)

            carModels = car_brand["carModels"]
            for carModel in carModels:
                car_model_name = carModel["name"]
                car_model_code = carModel["typeCode"]
                # print(car_model_name)
                # print(car_model_code)

                if CarModel.objects.filter(car_mark=car_mark,
                                           name=car_model_name,
                                           code=car_model_code).exists():
                    car_model = CarModel.objects.filter(car_mark=car_mark,
                                                        name=car_model_name,
                                                        code=car_model_code).first()
                else:
                    car_model = CarModel.objects.create(car_mark=car_mark, name=car_model_name,
                                                        code=car_model_code)

                car_model.car_mark = car_mark
                car_model.name = car_model_name
                car_model.code = car_model_code
                car_model.save()
