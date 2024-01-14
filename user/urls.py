from django.urls import re_path, path

from user.views import ProfileView, UsersView, UserDatatableView

urlpatterns = [
    re_path(r'^profilim', ProfileView.as_view(), name="profile"),
    path('users', UsersView.as_view(), name="users"),
    re_path(r'^users/(?P<user_pk>[\w-]+)', UsersView.as_view(), name="users_detail"),

    re_path(r'^datatable/users/', UserDatatableView.as_view(), name="users"),


]
