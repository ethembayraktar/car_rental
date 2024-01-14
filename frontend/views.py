import logging
import sys

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import View
from drf_yasg.renderers import OpenAPIRenderer, SwaggerUIRenderer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from kampanya.models import Kampanya
from utils.schemas import authtoken_request_body, authtoken_response_body
from utils.util import validate_recaptche


def handler404(request, exception="", template_name='errors/errorPage404.html'):
    type_, value, traceback = sys.exc_info()
    context = {
        "name": "404",
        "message": f"PAGE NOT FOUND! {value}"
    }

    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request), status=404)


def handler500(request, exception="", template_name='errors/errorPage500.html'):
    type_, value, traceback = sys.exc_info()
    context = {
        "name": "500",
        "message": f"500 Internal Server Error !=== > {value}"
    }

    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request), status=500)


def handler501(request, exception="", template_name='errors/errorPage501.html'):
    type_, value, traceback = sys.exc_info()
    context = {
        "name": "501",
        "message": f"501 Not Implemented !=== > {value}"
    }
    template = loader.get_template(template_name)
    return HttpResponse(template.render(context, request))


class UyelikSozlesmesiView(View):
    def get(self, request, page_name=None):
        context = {
            "active": ["#home"],
        }
        template = loader.get_template(f'uyelik_sozlesmesi.html')
        return HttpResponse(template.render(context, request))


class IndexView(View):
    def get(self, request, page_name=None):
        context = {
            "active": ["#home"],
            "kampanyalar": Kampanya.objects.filter(is_active=True, is_deleted=False,
                                                   started_at__lte=timezone.now(),
                                                   end_at__gte=timezone.now(),
                                                   ).order_by('order')
        }
        template = loader.get_template(f'index.html')
        return HttpResponse(template.render(context, request))


class IndexView2(View):
    def get(self, request, page_name=None):
        context = {
            "active": ["#home"],
            "kampanyalar": Kampanya.objects.filter(is_active=True, is_deleted=False,
                                                   started_at__lte=timezone.now(),
                                                   end_at__gte=timezone.now(),
                                                   ).order_by('order')
        }
        template = loader.get_template(f'index2.html')
        return HttpResponse(template.render(context, request))


class EnIndexView(View):
    def get(self, request, page_name=None):
        context = {
            "active": ["#home"],
        }
        template = loader.get_template(f'en.html')
        return HttpResponse(template.render(context, request))


class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []
    renderer_classes = [OpenAPIRenderer, SwaggerUIRenderer]

    @swagger_auto_schema(request_body=authtoken_request_body, responses=authtoken_response_body)
    def post(self, request):
        if Token.objects.filter(key=request.data["token"]).exists():
            auth_token = Token.objects.filter(key=request.data["token"]).first()
            user = auth_token.user
            auth_login(request, user)

            request.session["status"] = "success",
            request.session["message"] = "Giriş başarılı..."
            # return Response({
            #         "status": "success",
            #         "message": _("Login is successfull.")
            # })
            return redirect("/packets/all")

        return Response({
            "success": False,
            "message": _("Token is NOT VALID.")
        }, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(View):
    def get(self, request):
        redirect_url = request.GET["next"] if "next" in request.GET else "/"
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            Token.objects.create(user=request.user)
            return redirect(redirect_url)

        else:
            context = {
                'menu_open': [], 'active': ['sisteme_giris'],
            }
            template = loader.get_template('hesap/bireysel-uye-ol.html')
            return HttpResponse(template.render(context, request))

    def post(self, request):
        redirect_url = request.GET["next"] if "next" in request.GET else "/"

        if True or validate_recaptche(request.POST.get('g-recaptcha-response')):
            email = request.POST['email']
            email = " ".join(email.lower().strip().split())
            password = request.POST['password']
            user = authenticate(username=email, password=password)
            if user and user.is_active:
                auth_login(request, user)
                request.session["status"] = "success",
                request.session["message"] = "Giriş başarılı..."
                return redirect(redirect_url)
            else:
                context = {
                    'status': 'error',
                    'message': "Kullanıcı Adı veya Şifre Eşleşmedi"}
                template = loader.get_template('hesap/giris.html')
                return HttpResponse(template.render(context, request))
        else:
            context = {
                'status': "error",
                'message': "Invalid reCAPTCHA. Lütfen captcheyi doğrulayınız"
            }
            template = loader.get_template('hesap/giris.html')
            return HttpResponse(template.render(context, request))


class ForgetPasswordView(View):
    def get(self, request):
        redirect_url = request.GET["next"] if "next" in request.GET else "/"
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            Token.objects.create(user=request.user)
            return redirect(redirect_url)

        else:
            context = {
                'menu_open': [], 'active': ['forget_password'],
            }
            template = loader.get_template('hesap/sifre-sifirla.html')
            return HttpResponse(template.render(context, request))

    def post(self, request):
        redirect_url = request.GET["next"] if "next" in request.GET else "/"

        if True or validate_recaptche(request.POST.get('g-recaptcha-response')):
            email = request.POST['email']
            email = " ".join(email.lower().strip().split())
            """
            send password reset email
            """
            request.session['status'] = "success"
            request.session['message'] = "Password Reset Email has been sent to your registered email address"

            return redirect(redirect_url)

        else:
            context = {
                'status': "error",
                'message': "Invalid reCAPTCHA. Lütfen captcheyi doğrulayınız"
            }
            template = loader.get_template('hesap/sifre-sifirla.html')
            return HttpResponse(template.render(context, request))


class LoginView(View):
    def get(self, request):
        redirect_url = request.GET["next"] if "next" in request.GET else "/"
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            Token.objects.create(user=request.user)
            return redirect(redirect_url)

        else:
            context = {
                'menu_open': [], 'active': ['sisteme_giris'],
            }
            template = loader.get_template('hesap/giris.html')
            return HttpResponse(template.render(context, request))

    def post(self, request):
        redirect_url = request.GET["next"] if "next" in request.GET else "/"

        if True or validate_recaptche(request.POST.get('g-recaptcha-response')):
            email = request.POST['email']
            email = " ".join(email.lower().strip().split())
            password = request.POST['password']
            user = authenticate(username=email, password=password)
            if user and user.is_active:
                auth_login(request, user)
                request.session["status"] = "success",
                request.session["message"] = "Giriş başarılı..."
                return redirect(redirect_url)
            else:
                context = {
                    'status': 'error',
                    'message': "Kullanıcı Adı veya Şifre Eşleşmedi"}
                template = loader.get_template('hesap/giris.html')
                return HttpResponse(template.render(context, request))
        else:
            context = {
                'status': "error",
                'message': "Invalid reCAPTCHA. Lütfen captcheyi doğrulayınız"
            }
            template = loader.get_template('hesap/giris.html')
            return HttpResponse(template.render(context, request))


class LogoutView(View):
    def get(self, request):
        try:
            Token.objects.filter(user=request.user).delete()
            logout(request)
        except Exception as e:
            logging.exception(e)

        context = {
            'menu_open': [],
            'active': ['sisteme_giris'],
        }

        return redirect("/login")
