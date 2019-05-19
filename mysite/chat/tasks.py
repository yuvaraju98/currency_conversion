
from .models import user_info,chat_table
from .forms import *
from django.shortcuts import redirect,render
from .storage import store
from . import views
from .forms import RegisterForm,login_form
from ibm_watson import ToneAnalyzerV3
import pandas as pd

tone_codes={
    'Anger':'&#x1F92C',
    'Joy':'&#x1F603',
    'Sadness':'&#x1F641'
}


def upload(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if len(user_info.objects.filter(email=email))-1:
        response=user_info.objects.create(name=name,email=email ,password=password,online=0)
        response.save()
        response = redirect('/login/')
        return response
    else:
        form = RegisterForm()
        return render(request, 'chat/basic2.html',{'form': form,'comment':"User already exists ,try loggin in"})


def check(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    validation=user_info.objects.get(email=email)
    if validation:
        if validation.password == password:
            store.obj=validation.name
            response = redirect('/chat/')
            return response
        else:
            response = views._form_view(request,'chat/login.html',login_form,comment='Credentials incorrect,try again!')
            return response
    else:
        response = views._form_view(request, 'chat/login.html', login_form, comment='Credentials incorrect,try again!')
        return response


def chatbox2(request,users):
    d=dict()
    for x in users:
        d[x.id]=x.name
    d=d.values()
    chats=list(chat_table.objects.filter())
    form= chat()
    return render(request,'chat.html',{'users':d,'chats':chats,'form':form})


def upload_chat_task(message):
    chat_table.objects.create(sender=store.obj,message=message)
    return 0


def get_tone(message):
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        iam_apikey='BVPvPTdkRTBlDjc5f51jZOLPW23C5xztbzdbMFcyFp_N',
        url='https://gateway-lon.watsonplatform.net/tone-analyzer/api'
    )

    tone_analysis = tone_analyzer.tone(
        {'text': message},
        content_type='application/json'
    ).get_result()
    result =tone_analysis
    code=''
    if result:
        print(result)
        y=pd.DataFrame(result['document_tone']['tones'])
        tone=y.loc[y['score']==y['score'].max(),'tone_name'].item()
        if tone in tone_codes.keys():
            code=tone_codes[tone]
    return code


def chatbox(request,users):
    d=dict()
    for x in list(user_info.objects.filter()):
        d[x.id]=x.name
    d=d.values()
    chats=list(chat_table.objects.filter())
    form= chat()
    dictionry={'users':d,'chats':chats,'form':form}
    return views.room(request,dictionry)