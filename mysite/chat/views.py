# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.shortcuts import redirect,render
from .forms import DataForm
from .tasks import upload



def _form_view(request, template_name='chat/basic2.html', form_class=DataForm,comment=''):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            pass
    else:
        form = form_class()
    return render(request, template_name, {'form': form,'comment':comment})


def basic(request,comment=''):
    return _form_view(request,comment=comment)

def uploads(request):
    return upload(request)


