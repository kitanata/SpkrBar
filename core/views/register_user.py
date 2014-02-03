import json
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login
from django.template import loader, Context
from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from core.helpers import send_html_mail
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

        user.user_permissions.add(
            Permission.objects.get(codename='add_talk'),
            Permission.objects.get(codename='change_talk'),
            Permission.objects.get(codename='delete_talk'),

            Permission.objects.get(codename='add_talkcomment'),
            Permission.objects.get(codename='change_talkcomment'),
            Permission.objects.get(codename='delete_talkcomment'),

            Permission.objects.get(codename='add_engagement'),
            Permission.objects.get(codename='change_engagement'),
            Permission.objects.get(codename='delete_engagement'),

            Permission.objects.get(codename='add_usertag'),
            Permission.objects.get(codename='add_talktag'),
            Permission.objects.get(codename='add_location'),

            Permission.objects.get(codename='add_userlink'),
            Permission.objects.get(codename='change_userlink'),
            Permission.objects.get(codename='delete_userlink'),

            Permission.objects.get(codename='add_talklink'),
            Permission.objects.get(codename='change_talklink'),
            Permission.objects.get(codename='delete_talklink'),

            Permission.objects.get(codename='add_talkslidedeck'),
            Permission.objects.get(codename='change_talkslidedeck'),
            Permission.objects.get(codename='delete_talkslidedeck'),

            Permission.objects.get(codename='add_talkvideo'),
            Permission.objects.get(codename='change_talkvideo'),
            Permission.objects.get(codename='delete_talkvideo'),

            Permission.objects.get(codename='add_talkendorsement'),
            Permission.objects.get(codename='delete_talkendorsement'),

            Permission.objects.get(codename='add_userfollowing'),
            Permission.objects.get(codename='delete_userfollowing'),

            Permission.objects.get(codename='change_spkrbaruser'),
            Permission.objects.get(codename='add_feedback'),
        )

        user.save()

        text = """
            Hi there! 
            
            I'm SpkrBot. I want to thank you for joining SpkrBar as a speaker. Did you know that with SpkrBar you can:

            <ul>
                <li>Host all the information about your talks in one place</li>
                <li>Find events you'd like to speak at and submit proposals to them</li>
                <li>Get great feedback on your talks by the people who attend them</li>
                <li>Find other talks like yours and learn from them</li>
            </ul>

            Oh, and before I forget, we are working on making the site better every day, so if you encounter any problems, have questions, or want to give us any feedback please send me an email and I'll automatically send it on to our developers. We read every email we get.

            Thanks again,
            SpkrBot @ Spkrbar.com
            """

        mes = email_template.render(Context({'message': text}))
        send_html_mail("Welcome to SpkrBar", text, mes, [user.email])

        user = authenticate(email=email, password=password)
        login(request, user)

        data = JSONRenderer().render(UserSerializer(user).data)
        return HttpResponse(data, content_type="application/json", status=201)
