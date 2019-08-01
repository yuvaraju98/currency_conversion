# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.shortcuts import redirect,render
from .forms import DataForm
from .tasks import upload,process
from .charts import LineChart



def _form_view(request, template_name='chat/basic2.html', form_class=DataForm,comment='',line_chart=LineChart({'label':0})):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            pass
    else:
        form = form_class()
    return render(request, template_name, {'form': DataForm,'comment':comment,'line_chart':line_chart})


def basic(request,comment=''):
    return _form_view(request,comment=comment)

def upload(request):
    points=process(request)
    print("response",points)
    return _form_view(request,comment='',line_chart=LineChart(points))


def dis(request):
    return render(request, 'chat/chart.html', {
            'line_chart': LineChart([1,2,3]),
        })


