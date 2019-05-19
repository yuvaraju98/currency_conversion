# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.basic, name='basic'),
    url(r'login/$', views.login, name='login'),
    url(r'room/$', views.room, name='room'),
    url(r'chat/$', views.chat, name='chat'),
    url(r'login_verify/$', views.login_check, name='login_validations'),
    url(r'upload/$', views.upload, name='uploading creds'),

]