import json
import logging
import sys

from django.apps import apps
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
from dotenv import load_dotenv
from drf_yasg.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from attachment.serializers import AttachmentSerializer
from user.filters import UserFilter
from user.models import User
from user.serializers import UserSerializer, CustomTokenObtainPairSerializer
from utils.constants import ACENTE, OTO_KURTARMA, OTO_KIRALAMA, OTO_LASTIKCI
from utils.permissions import IsSuperuser, IsOwner
from utils.util import validate_recaptche, get_secret_key, MyModelViewSet

load_dotenv()


def handler404(request, exception="", template_name='errors/errorPage404.html'):
    type_, value, traceback = sys.exc_info()
    context = {
        "name": "404",
        "mail": f"PAGE NOT FOUND! {value}"
    }

    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request), status=404)


def handler500(request, exception="", template_name='errors/errorPage500.html'):
    type_, value, traceback = sys.exc_info()
    context = {
        "name": "500",
        "mail": f"500 Internal Server Error !=== > {value}"
    }

    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request), status=500)


def handler501(request, exception="", template_name='errors/errorPage501.html'):
    type_, value, traceback = sys.exc_info()
    context = {
        "name": "501",
        "mail": f"501 Not Implemented !=== > {value}"
    }
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request))


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/admin/")
        else:
            context = {
                'menu_open': [],
                'active': ['sisteme_giris'],
            }
            template = loader.get_template('assist/page-login.html')
            return HttpResponse(template.render(context, request))

    def post(self, request):
        if validate_recaptche(request.POST.get('g-recaptcha-response')):
            username = request.POST['username']
            username = " ".join((username.lower().strip()).split())
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                auth_login(request, user)
                user.login_secret = get_secret_key()
                user.save()

                request.session["status"] = "success"
                request.session["message"] = "Giriş başarılı.."

                return redirect("/")
            else:
                return redirect("/login")
        else:
            context = {
                'status': "error",
                'mail': "Invalid reCAPTCHA. Lütfen captcheyi doğrulayınız"
            }
            request.session["status"] = "error"
            request.session["message"] = "Invalid reCAPTCHA. Lütfen captcheyi doğrulayınız"

            return redirect("/login")


class LogoutApiView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        return redirect("/")


@csrf_exempt
@login_required(login_url="/login/")
def delete_object(request, uid, login_secret):
    if request.method == "POST" and str(request.user.id) == uid:
        context = {}
        model_str = request.POST.get("model") if "model" in request.POST else None
        pk = request.POST.get("pk") if "pk" in request.POST else None

        if model_str is None or pk is None:
            context = {
                "status": "error",
                "mail": "Model ya da pk in düzgün şekilde set edildiğine emin olunuz"
            }
            return JsonResponse(context, safe=False)

        try:
            if model_str in ["User", "Group"]:
                model = apps.get_model('auth', model_str)
            else:
                model = apps.get_model('formtype', model_str)
            my_type = request.POST.get("my_type") if "my_type" in request.POST else None
            deleted_items = 0
            queryset = []
            if my_type is None:
                item = model.objects.filter(pk=pk).first()
                item.delete()
                context["status"] = "success"
                context["mail"] = model_str + "  modeline ait " + str(pk) + " pk li item başarı ile silindi! "
            else:
                if model_str == "NotificationUserRelation":
                    context["mail"] = "{} adet bildirimler başarı ile silindi!"
                    if my_type is not None and my_type == "all":
                        queryset = model.objects.filter(user=request.user, is_deleted=False)
                    elif my_type is not None and my_type == "list":
                        ids = json.loads(pk)
                        queryset = model.objects.filter(pk__in=ids, user=request.user, is_deleted=False)
                    else:
                        queryset = model.objects.filter(pk=pk, user=request.user).first()

                elif model_str == "MessageUserRelation":
                    context["mail"] = "{} adet mesajlar başarı ile silindi!"
                    if my_type is not None and my_type == "all":
                        queryset = model.objects.filter(recipient=request.user, is_deleted=False)
                    elif my_type is not None and my_type == "list":
                        ids = json.loads(pk)
                        queryset = model.objects.filter(pk__in=ids, recipient=request.user, is_deleted=False)
                    else:
                        queryset = model.objects.filter(pk=pk, recipient=request.user)
                for relation in queryset:
                    relation.is_deleted = True
                    relation.delete_at = timezone.now()
                    relation.save()
                    deleted_items += 1

                context["status"] = "success"
                context["mail"] = context["mail"].format(deleted_items)

        except Exception as e:
            context = {
                "status": "error",
                "mail": "Bir hata oluştu==>" + str(e),
            }
        return JsonResponse(context)

    else:
        context = {
            "status": "error",
            "mail": "Bu işlemi yapma yetkiniz yoktur.",
        }
        return JsonResponse(context)


@login_required(login_url="/login/")
def read_object(request, uid, login_secret):
    if request.method == "POST" and str(request.user.id) == uid:
        # pprint.pprint(request.POST)
        context = {}

        model_str = request.POST.get("model") if "model" in request.POST else None
        ids = request.POST.get("ids") if "ids" in request.POST else None
        if model_str is None or ids is None:
            context = {
                "status": "error",
                "mail": "Model ya da ids in düzgün şekilde set edildiğine emin olunuz"
            }
            return JsonResponse(context, safe=False)

        try:
            model = apps.get_model('formtype', model_str)
            my_type = request.POST.get("my_type")
            read_items = 0
            if ids and ids == "all":
                queryset = model.objects.filter(user=request.user, is_deleted=False, is_read=False)
            elif my_type == "list":
                queryset = model.objects.filter(id__in=ids, is_deleted=False, user=request.user, is_read=False)
            else:
                queryset = model.objects.filter(id=ids, is_deleted=False, user=request.user, is_read=False)

            for relation in queryset:
                relation.is_read = True
                relation.read_at = timezone.now()
                relation.save()
                read_items += 1
            context["status"] = "success"
            context["mail"] = "Bildirimler başarı ile okundu! ==>" + str(read_items)
        except Exception as e:
            context = {
                "status": "error",
                "mail": "Bir hata oluştu==>" + str(e),
            }

        return JsonResponse(context)

    else:
        context = {
            "status": "error",
            "mail": "Login credidentials not satisfied.",
        }

        return JsonResponse(context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        template = loader.get_template(f'assist/{request.user.role}/profile.html')


        context = {
            'menu_open': [],
            'active': [],
        }
        return HttpResponse(template.render(context, request))

    def post(self, request):
        if validate_recaptche(request.POST.get('g-recaptcha-response')):
            username = request.POST['username']
            username = " ".join((username.lower().strip()).split())
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                auth_login(request, user)
                user.login_secret = get_secret_key()
                user.save()

                request.session["status"] = "success"
                request.session["message"] = "Giriş başarılı.."

                return redirect("/")
            else:
                return redirect("/login")
        else:
            context = {
                'status': "error",
                'mail': "Invalid reCAPTCHA. Lütfen captcheyi doğrulayınız"
            }
            request.session["status"] = "error"
            request.session["message"] = "Invalid reCAPTCHA. Lütfen captcheyi doğrulayınız"

            return redirect("/login")


class UsersView(LoginRequiredMixin, View):
    def get(self, request, user_pk=None):
        if request.user.is_superuser:
            template = None
            context = {
                'menu_open': [],
                'active': ["#users"],
            }
            if user_pk:
                context["my_user"] = User.objects.filter(pk=user_pk).first()
                template = loader.get_template('assist/super_admin/user_private.html')
            else:
                template = loader.get_template('assist/super_admin/users.html')

            return HttpResponse(template.render(context, request))
        return Response(status=403)

    def post(self, request):
        if validate_recaptche(request.POST.get('g-recaptcha-response')):
            username = request.POST['username']
            username = " ".join((username.lower().strip()).split())
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                auth_login(request, user)
                user.login_secret = get_secret_key()
                user.save()

                request.session["status"] = "success"
                request.session["message"] = "Giriş başarılı.."

                return redirect("/")
            else:
                return redirect("/login")
        else:
            context = {
                'status': "error",
                'mail': "Invalid reCAPTCHA. Lütfen captcheyi doğrulayınız"
            }
            request.session["status"] = "error"
            request.session["message"] = "Invalid reCAPTCHA. Lütfen captcheyi doğrulayınız"

            return redirect("/login")


class UserViewSet(MyModelViewSet):
    queryset = User.objects.filter(is_active=True, is_deleted=False)
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter
    CACHE_KEY_PREFIX = "user-view"
    ordering_fields = ['id', 'role', 'email', 'is_active', 'is_staff', 'is_mobile_verified', 'first_name', 'last_name']
    search_fields = ['id', 'role', 'email', 'is_active', 'is_staff', 'is_mobile_verified', 'first_name', 'last_name']
    lookup_field = 'pk'

    permission_classes_per_method = {
        # except for list and retrieve where both users with "write" or "read-only"
        # permissions can access the endpoints.
        "list": [IsSuperuser],
        "retrieve": [IsSuperuser | IsOwner],
        "create": [IsSuperuser],
        "update": [IsSuperuser | IsOwner],
        "partial_update": [IsSuperuser | IsOwner],
        "destroy": [IsSuperuser],
    }

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        If a user doesn't send required areas, it means that partial update
        """
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    """
    Admin istatistik apisi için :  Toplam tedarikçi, Toplam ürün, Toplam sipariş, Toplam kullanıcı, onay bekleyen vendor 
     ve onay bekleyen ürün sayılarına ihtiyacım var. 
     Birde grafik için son bir haftalık siparişler içerisinden toplam sipariş, 
     iptal edilen sipariş ve iade edilen sipariş sayılarına ihtiyacım var. 
     Müsait olduğunuzda bakabilir misiniz acaba ?
    """


class UserDatatableView(LoginRequiredMixin, BaseDatatableView):
    def get_initial_queryset(self):
        self.max_display_length = 20
        self.model = User
        self.columns = ["id",
                        "avatar",
                        "first_name",
                        "last_name",
                        "tckn",
                        "email",
                        "phone",
                        "role",
                        "date_joined",
                        "is_active"]

        self.order_columns = ["id",
                              "avatar",
                              "first_name",
                              "last_name",
                              "tckn",
                              "email",
                              "phone",
                              "role",
                              "date_joined",
                              "is_active"]
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.none()

    def filter_queryset(self, qs):
        try:
            my_search = self.request.GET.get('search[value]', None)
            if my_search and not my_search == "":
                q = (Q(id__icontains=my_search) |
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
                "avatar": AttachmentSerializer(item.avatar).data if item.avatar else None,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "email": item.email,
                "tckn": item.tckn,
                "phone": item.phone,
                "role": item.role,
                "date_joined": item.date_joined
            })
            i += 1
        return json_data


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]
    serializer_class = CustomTokenObtainPairSerializer
