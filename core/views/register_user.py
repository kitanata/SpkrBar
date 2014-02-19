import json
from django.contrib.auth import authenticate, login
from django.template import loader, Context
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.html import strip_tags
from rest_framework.renderers import JSONRenderer

from core.helpers import send_html_mail, assign_basic_permissions
from core.models import SpkrbarUser
from core.serializers import RegisterUserSerializer, UserSerializer

email_template = loader.get_template('mail/register.html')

def register_user(request):
    data = json.loads(request.body)
    serializer = RegisterUserSerializer(data=data)
    
    if serializer.is_valid():
        email = serializer.data['email'].lower()
        full_name = serializer.data['full_name']

        password = serializer.data['password']
        confirm = serializer.data['confirm']

        if password != confirm:
            return HttpResponse(
                json.dumps({'error': "password_match"}),
                content_type="application/json", status=400)
        try:
            user = SpkrbarUser.objects.create_user(email, password)
            user.save()
        except IntegrityError:
            return HttpResponse(
                json.dumps({'error': "email_taken"}),
                content_type="application/json", status=400)

        user.full_name = full_name
        user.about_me = serializer.data['about_me']
        user.is_event_manager = serializer.data['is_event_planner']
        user.plan_name = serializer.data['plan_name']

        assign_basic_permissions(user)

        user.save()

        mes = email_template.render(Context({'name': user.full_name}))
        send_html_mail("Welcome to SpkrBar", strip_tags(mes), mes, [user.email])

        user = authenticate(email=email, password=password)
        login(request, user)

        data = JSONRenderer().render(UserSerializer(user).data)
        return HttpResponse(data, content_type="application/json", status=201)
