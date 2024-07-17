from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from .models import User  # Import your User model
from mediaproject import settings
from django.shortcuts import render

# Create your views here.



from django.core.mail import send_mail , EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect

import random
from django.core.mail import send_mail , EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect

from django.conf import settings

from .token import generate_token
from rest_framework import status
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode

class Signup(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        # profile_img = request.data.get('profile_img')
        sub_admin = request.data.get('sub_admin', False)  
        phone_number = request.data.get('phone_number')
        roles = request.data.get('roles')

        if User.objects.filter(username=username).exists():
            return Response({"Message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # if User.objects.filter(email=email).exists():
        #     return Response({'Message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Creating the user with the User model
        myuser = User.objects.create_user(username=username,password=password,email=email,phone_number=phone_number)

        
        myuser.sub_admin = sub_admin
        myuser.phone_number = phone_number
        myuser.roles = roles
        myuser.is_active = False
        print(myuser)

        myuser.save()

        curent_site=get_current_site(request)
        email_subject = 'confirmatiom mail @ MEDIA HUB'
        message2=render_to_string('activation_mail.html',{
            'name':myuser.username,
            'domain':curent_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser),
        })
        print("here")
        email = EmailMessage(
            email_subject,message2,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )
        email.fail_silently=True
        email.send()
        return Response({'message' : 'user craeted successfully'},status=status.HTTP_201_CREATED)

    
def activate(request,uid64,token):
    try:
        uid= force_str(urlsafe_base64_decode(uid64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        return HttpResponseRedirect(settings.SITE_URL_AUTH)
    else:
        return render(request,'authentication/activation_failed.html')

# class RegisterView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

