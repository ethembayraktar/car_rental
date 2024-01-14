from django import forms
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import int_to_base36
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator


class CustomPasswordResetForm(PasswordResetForm):
    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, request=None,
             email_subject_name='registration/password_reset_subject.txt', **kwargs):

        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override

            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            render_html = render_to_string(email_template_name, c)
            msg = EmailMultiAlternatives("", strip_tags(render_html), None, [user.email])
            msg.attach_alternative(render_html, "text/html")
            msg.send()


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control input-lg'}),

    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Password', 'type': 'password', 'class': 'form-control input-lg'}),

    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        return password
