from django.conf.urls import url

from . import consumers
from django.conf.urls import include, url

websocket_urlpatterns = [
    url(r'^ws/chat/chatroom/$', consumers.ChatConsumer),

]