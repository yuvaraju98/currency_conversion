# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.basic, name='basic'),
    url(r'upload/$', views.upload, name='uploading creds'),
]