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
        myuser.is_active = True
        print(myuser)

        myuser.save()

       
        return Response({'message' : 'user craeted successfully'},status=status.HTTP_201_CREATED)

    



