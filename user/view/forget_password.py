from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from user.models import Profile , Services , Categorys , Employee , Choose 
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from ..serializers import ProfileSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Forget_password(APIView):
    def post(self , request):
        email = request.data.get('email')

        # checking data
        if not email:
            return Response({"error":"enter email"}, status.HTTP_400_BAD_REQUEST)
        
        try:
            # if user not found
            user_obj = User.objects.filter(email = email).first()
            if user_obj is None:
                return Response({"error":"User not found"}, status.HTTP_400_BAD_REQUEST)
            
            
            profile_obj = Profile.objects.filter(user = user_obj).first()
            if profile_obj is None:
                return Response({"error":"Please not login with admin account"}, status.HTTP_400_BAD_REQUEST)
            
            # generating unique no.
            auth_token = str(uuid.uuid4())
            profile_obj.auth_token = auth_token
            profile_obj.save()

            # sending mail
            send_mail_for_reset_password(email , auth_token)    
            return Response({"status":"forget mail sended to users mail Please check"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

# it send mail
def send_mail_for_reset_password(email , token):
    subject = 'Your accounts need to reset password'
    message = f'Hi paste the link to reset the password http://localhost:8000/reset_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )



class Reset_password(APIView):
    def post(self , request ,  auth_token):
        if request.user.is_authenticated:
            user_obj = request.user
            profile_obj = Profile.objects.filter(user = user_obj).first()
            if profile_obj is None:
                return Response({"error":"Please not login with admin account"}, status.HTTP_400_BAD_REQUEST)
            return Response({"error":"Please first logout"}, status.HTTP_400_BAD_REQUEST)
        
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not password or not confirm_password:
            return Response({"error":"Please enter password"}, status.HTTP_400_BAD_REQUEST)
        elif len(password) < 6 or len(confirm_password) < 6:
            return Response({"error":"Password length must be greater than 6 character"}, status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({"error":"Password and confirm password are different"}, status.HTTP_400_BAD_REQUEST)

        try:
            profile_obj = Profile.objects.filter(auth_token = auth_token).first()
            if profile_obj:
                # it reset password
                username = profile_obj.user.username
                user_obj = User.objects.filter(username = username).first()
                data = {
                    "password" : make_password(request.data.get("password"))
                }
                serializer = UserSerializer(user_obj , data = data , partial=True)
                if not serializer.is_valid():
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

                serializer.save()

                return Response({"status":"your password is reset please login"}, status=status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return redirect('/')


class Verify(APIView):
    def get(self , request , auth_token):
        try:
            profile_obj = Profile.objects.filter(auth_token = auth_token).first()

            # checking is there is user created there account or not
            if profile_obj:
                # it check it verified or not
                if profile_obj.is_verified:
                    return Response({"error":"User already verified"}, status.HTTP_400_BAD_REQUEST)
                profile_obj.is_verified = True
                profile_obj.save()
                return Response({"status":"User verified please login"}, status=status.HTTP_200_OK)
            else:
                return Response({"error":"Admin cannot use this functionality please login user account"}, status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print(e)
            return redirect('/')


# def forget_password(req ):
    
#     # it check user login with admin account 
#     if req.user.is_authenticated:
#         user_obj = req.user
#         profile_obj = Profile.objects.filter(user = user_obj).first()
#         if profile_obj is None:
#             auth.logout(req)
#             return redirect('/')
#         return redirect('/')

#     if req.method == "GET":
#         return render(req, "user/forget_password.html")

#     elif req.method == 'POST':
#         email = req.POST.get('email')

#         # checking data
#         if not email:
#             messages.error(req, "Please enter email")
#             return redirect("/forget_password")

#         try:
#             # if user not found
#             user_obj = User.objects.filter(email = email).first()
#             if user_obj is None:
#                 messages.error(req, 'User not found.')
#                 return redirect('/forget_password')
            
            
#             profile_obj = Profile.objects.filter(user = user_obj).first()
#             if profile_obj is None:
#                 return redirect('/login')
            
#             # generating unique no.
#             auth_token = str(uuid.uuid4())
#             profile_obj.auth_token = auth_token
#             profile_obj.save()

#             # sending mail
#             send_mail_for_reset_password(email , auth_token)    
#             messages.success(req, 'Email send succesfully check your email.')

#             return render(req, f"user/check_mail_send.html" , {'email':email})

#         except Exception as e:
#             print(e)

# # it send mail
# def send_mail_for_reset_password(email , token):
#     subject = 'Your accounts need to reset password'
#     message = f'Hi paste the link to reset the password http://localhost:8000/reset_password/{token}'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message , email_from ,recipient_list )


# it check email verification of user 


# def verify(request , auth_token):

#     try:
#         profile_obj = Profile.objects.filter(auth_token = auth_token).first()

#         # checking is there is user created there account or not
#         if profile_obj:
#             # it check it verified or not
#             if profile_obj.is_verified:
#                 messages.error(request, 'Your account is already verified.')
#                 return redirect('/login')
#             profile_obj.is_verified = True
#             profile_obj.save()
#             messages.success(request, 'Your account has been verified.')
#             return redirect('/login')
#         else:
#             messages.success(request, 'Admin cannot use this functionality please login user account.')
#             return redirect('/login')
#     except Exception as e:
#         print(e)
#         return redirect('/')



# def reset_password(req , auth_token):
    
#     # it check user login with admin account 
#     if req.user.is_authenticated:
#         user_obj = req.user
#         profile_obj = Profile.objects.filter(user = user_obj).first()
#         if profile_obj is None:
#             auth.logout(req)
#             return redirect('/login')
#         return redirect('/')

#     if req.method == "GET":
#         return render(req, "user/reset_password.html")

#     elif req.method == 'POST':
#         password = req.POST.get('password')
#         confirm_password = req.POST.get('confirm_password')

#         # it check data
#         if not password or not confirm_password:
#             messages.error(req, "Please enter password")
#             return redirect(f"/reset_password/{auth_token}")
#         elif len(password) < 6 or len(confirm_password) < 6:
#             messages.error(req, "Password length must be greater than 6 character")
#             return redirect(f"/reset_password/{auth_token}")

#         if password != confirm_password:
#             messages.error(req, 'Password and confirm password are different.')
#             return redirect('/forget_password')

#         try:
#             profile_obj = Profile.objects.filter(auth_token = auth_token).first()
#             if profile_obj:
#                 # it reset password
#                 username = profile_obj.user.username
#                 user_obj = User.objects.filter(username = username).first()
#                 user_obj.set_password(password)
#                 user_obj.save()
#                 messages.success(req, 'Your password is changed.')
#                 return redirect('/login')
#             else:
#                 messages.success(req, 'Admin cannot use this functionality please login user account.')
#                 return redirect('/forget_password')
#         except Exception as e:
#             print(e)
#             return redirect('/')