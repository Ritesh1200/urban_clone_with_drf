from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from user.models import Profile , Services , Categorys , Employee , Choose 
from django.contrib.auth.decorators import login_required


from ..serializers import ChooseSerializer, ProfileSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Update(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self , request ):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        address = request.data.get('address')

        # checking all data 
        if not username:
            return Response({"error":"Please enter username"}, status.HTTP_400_BAD_REQUEST)
        elif len(username) < 4:
            return Response({"error":"username length must be greater than 4"}, status.HTTP_400_BAD_REQUEST)
        elif not email:
            return Response({"error":"Please enter email"}, status.HTTP_400_BAD_REQUEST)
        elif len(email) < 5:
            return Response({"error":"email must be greater than 5"}, status.HTTP_400_BAD_REQUEST)
        elif not address:
            return Response({"error":"Please enter address"}, status.HTTP_400_BAD_REQUEST)
        elif not password:
            return Response({"error":"Please enter password"}, status.HTTP_400_BAD_REQUEST)
        elif len(password) < 6:
            return Response({"error":"password length must be greater than 6"}, status.HTTP_400_BAD_REQUEST)

        try:
            # creating user
            user_obj = request.user
            user_obj.username = username 
            user_obj.email = email 
            user_obj.set_password(password)
            user_obj.save()
            # creating profile of user
            profile_obj = Profile.objects.filter(user = user_obj ).first()
            profile_obj.address = address
            profile_obj.save()

            return Response({"stat":"user data updated"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return redirect("/profile")


# @login_required(login_url='/login')
# def update(req ):
#     user_obj = req.user
#     profile_obj = Profile.objects.filter(user = user_obj).first()
#     if profile_obj is None:
#         return redirect('/login')

    
#     if req.method == "GET":
#         return render(req, "user/update.html",{"name":user_obj.username,"email":user_obj.email,"address":profile_obj.address} )
    
#     if req.method == "POST":

#         username = req.POST.get('username')
#         email = req.POST.get('email')
#         password = req.POST.get('password')
#         address = req.POST.get('address')

#         # checking all data 
#         if not username:
#             messages.error(req, 'Please fill username.')
#             return render(req, "user/update.html")
#         elif len(username) < 4:
#             messages.error(req, 'Username length must be greater than 4 letter.')
#             return render(req, "user/update.html")
#         elif not email:
#             messages.error(req, 'Please fill email.')
#             return render(req, "user/update.html")
#         elif len(email) < 5:
#             messages.error(req, 'Email length must be greater than 4 letter.')
#             return render(req, "user/update.html")
#         elif not address:
#             messages.error(req, 'Please fill address.')
#             return render(req, "user/update.html")
#         elif not password:
#             messages.error(req, 'Please fill password.')
#             return render(req, "user/update.html")
#         elif len(password) < 6:
#             messages.error(req, 'Password must greater than 6 character')
#             return render(req, "user/update.html")

#         try:
#             # it check username is already taken or not
#             if User.objects.filter(username = username).first():
#                 messages.success(req, 'Username is taken.')
#                 return render(req, "user/update.html")

#             # it check email is already taken or not
#             if User.objects.filter(email = email).first():
#                 messages.success(req, 'Email is taken.')
#                 return render(req, "user/update.html")
            
#             # creating user
#             user_obj.username = username 
#             user_obj.email = email 
#             user_obj.set_password(password)
#             user_obj.save()
#             # creating profile of user
#             profile_obj = Profile.objects.filter(user = user_obj ).first()
#             profile_obj.address = address
#             profile_obj.save()

#             user = auth.authenticate(username = username , password = password)
#             auth.login(req , user)
#             messages.success(req, 'Update succesfull')
#             return redirect("/profile")

#         except Exception as e:
#             print(e)
#             return redirect("/profile")

    