from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from user.models import Profile , Services , Categorys , Employee , Choose 


from ..serializers import ProfileSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class Login(ObtainAuthToken):
    def post(self , request):
        if request.user.is_authenticated:
            user_obj = request.user
            profile_obj = Profile.objects.filter(user = user_obj).first()
            if profile_obj is None:
                auth.logout(request)
                return Response({"error":"Admin cannot use this functionality please login user account."}, status.HTTP_400_BAD_REQUEST)
        
        username = request.data.get('username')
        password = request.data.get('password')

        # checking data
        if not username:
            return Response({"error":"Please enter username"}, status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({"error":"Please enter password"}, status.HTTP_400_BAD_REQUEST)

        # it checks username in User 
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            return Response({"error":"user not found"}, status.HTTP_400_BAD_REQUEST)

        profile_obj = Profile.objects.filter(user = user_obj ).first()
        if profile_obj is None:
            return Response({"error":"Admin cannot use this functionality please login user account"}, status.HTTP_400_BAD_REQUEST)
        
        # it check the user is email verified or not
        else:
            if not profile_obj.is_verified:
                return Response({"error":"Profile is not verified check your mail"}, status.HTTP_400_BAD_REQUEST)

                

        # it check the username and password 
        user = auth.authenticate(username = username , password = password)
        if user is not None:
            
        #     # user loged in
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "username": user.username,
                "password": request.data.get("password"),
                "token" : token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error":"invalid cridenctial"}, status.HTTP_400_BAD_REQUEST)




# def login(req):

#     # it check user login with admin account 
#     if req.user.is_authenticated:
#         user_obj = req.user
#         profile_obj = Profile.objects.filter(user = user_obj).first()
#         if profile_obj is None:
#             auth.logout(req)
#             messages.error(req, 'Admin cannot use this functionality please login user account.')
#             return redirect('/')
#         return redirect('/')

#     if req.method == "GET":
#         return render(req, "user/login.html")

#     elif req.method == "POST":
#         username = req.POST['username']
#         password = req.POST['password']

#         # checking data
#         if not username:
#             messages.error(req, 'Please fill username.')
#             return render(req, "user/login.html")
#         elif not password:
#             messages.error(req, 'Please fill password.')
#             return render(req, "user/login.html")

#         # it checks username in User 
#         user_obj = User.objects.filter(username = username).first()
#         if user_obj is None:
#             messages.error(req, 'User not found.')
#             return redirect('/login')

#         profile_obj = Profile.objects.filter(user = user_obj ).first()
#         if profile_obj is None:
#             messages.error(req, 'Admin cannot use this functionality please login user account.')
#             return redirect('/login')
        
#         # it check the user is email verified or not
#         else:
#             if not profile_obj.is_verified:
#                 messages.error(req, 'Profile is not verified check your mail.')
#                 return redirect('/login')

#         # it check the username and password 
#         user = auth.authenticate(username = username , password = password)
#         if user is not None:
            
#             # user loged in
#             auth.login(req , user)
#             messages.success(req , 'user login successfully')
#             return redirect('/')
#         else:
#             messages.error(req , 'invalid cridenctial')

#     return render(req , 'user/login.html' )


