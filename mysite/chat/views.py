# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.shortcuts import redirect,render
from .forms import RegisterForm,login_form
from . import tasks
from .storage import store


def _form_view(request, template_name='chat/basic2.html', form_class=RegisterForm,comment=''):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            pass
    else:
        form = form_class()
    return render(request, template_name, {'form': form,'comment':comment})


def basic(request,comment=''):
    return _form_view(request,comment=comment)


def upload(request):
    return tasks.upload(request)


def login(request):
    return _form_view(request,'chat/login.html',login_form)


def login_check(request):
    return tasks.check(request)


def chat(request):
    if store.obj=='unknown':
        response = redirect('/login')
        return response
    return tasks.chatbox(request,['Unknown'])


def room(request,dictionary):
    dictionary.update({'room_name_json': mark_safe(json.dumps("chatroom"))})
    return render(request, 'chat/chat.html', dictionary)