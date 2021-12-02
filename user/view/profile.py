from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from user.models import Profile
from django.contrib.auth.decorators import login_required

from ..serializers import ProfileSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Userprofile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self , request):

        user_obj = request.user
        serializer = UserSerializer(user_obj )
        return Response(serializer.data , status= status.HTTP_200_OK)


# @login_required(login_url='/login')
# def profile(req):
    
#     # it check user login with admin account 
#     user_obj = req.user
#     profile_obj = Profile.objects.filter(user = user_obj).first()
#     if profile_obj is None:
#         return redirect('/login')
    
#     return render(req, 'user/profile.html' , {'profile':profile_obj})
