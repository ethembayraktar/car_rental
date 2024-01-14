from django.urls import re_path, path

from frontend.views import IndexView, LoginView, LogoutView, EnIndexView, RegisterView, IndexView2, \
    UyelikSozlesmesiView, ForgetPasswordView

urlpatterns = [
    re_path(r'^$', IndexView.as_view(), name="assist_admin"),
    re_path(r'^en', EnIndexView.as_view(), name="enassist_admin"),
    path('index', IndexView.as_view(), name="index"),
    path('index2', IndexView2.as_view(), name="index2"),
    re_path(r'^home/$', IndexView.as_view(), name='home'),

    re_path(r'^forget-password', ForgetPasswordView.as_view(), name='forgetpassword'),
    re_path(r'^login', LoginView.as_view(), name='login'),
    re_path(r'^register', RegisterView.as_view(), name='register'),
    re_path(r'^logout', LogoutView.as_view(), name='logout'),

    re_path(r'^$', IndexView.as_view(), name="assist_admin"),
    re_path(r'^index', IndexView.as_view(), name="index"),
    re_path(r'^home/$', IndexView.as_view(), name='home'),
    path('uyelik-sozlesmesi', UyelikSozlesmesiView.as_view(), name='uyelik-sozlesmesi'),

]
