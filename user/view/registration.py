from django.contrib.auth.models import User
from user.models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail

from ..serializers import ProfileSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# register page

class Register(APIView):
    
    def post(self , request):
        
        if request.user.is_authenticated:
            user_obj = request.user
            profile_obj = Profile.objects.filter(user = user_obj).first()
            if profile_obj is None:
                return Response({"error":"Please not login with admin account"}, status.HTTP_400_BAD_REQUEST)
            return Response({"error":"Please first logout"}, status.HTTP_400_BAD_REQUEST)
        
        
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
            # it check username is already taken or not
            if User.objects.filter(username = username).first():
                return Response({"error":"Username is taken"}, status.HTTP_400_BAD_REQUEST)

            # it check email is already taken or not
            if User.objects.filter(email = email).first():
                return Response({"error":"Email is taken"}, status.HTTP_400_BAD_REQUEST)
            
            # creating user
            userserializer = UserSerializer(data = request.data)
            if not userserializer.is_valid():
                return Response(userserializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            userserializer.save()
            auth_token = str(uuid.uuid4())

            # creating profile of user
            
            user_obj = User.objects.filter(username = username).first()
            data = {
                "user" : user_obj.id,
                "auth_token" : auth_token,
                "address" : address
            }
            # profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token , address=address)
            # profile_obj.save()
            profileserializer = ProfileSerializer(data = data )
            print("iiii")
            if not profileserializer.is_valid():
                print("hhh")
                return Response(profileserializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            profileserializer.save()
            # send mail to user for authenticate 
            send_mail_after_registration(email , auth_token)
            return Response({"status":"Email sended to mail Please verify"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)



# it send email to user with token
def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://localhost:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


# def register(request):
    
#     # it check user login with admin account 
#     if request.user.is_authenticated:
#         user_obj = request.user
#         profile_obj = Profile.objects.filter(user = user_obj).first()
#         if profile_obj is None:
#             return redirect('/login')
#         return redirect('/')


#     if request.method == "GET":
#         return render(request, "user/register.html")

#     elif request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         address = request.POST.get('address')

#         # checking all data 
#         if not username:
#             messages.error(request, 'Please fill username.')
#             return render(request, "user/register.html")
#         elif len(username) < 4:
#             messages.error(request, 'Username length must be greater than 4 letter.')
#             return render(request, "user/register.html")
#         elif not email:
#             messages.error(request, 'Please fill email.')
#             return render(request, "user/register.html")
#         elif len(email) < 5:
#             messages.error(request, 'Email length must be greater than 4 letter.')
#             return render(request, "user/register.html")
#         elif not address:
#             messages.error(request, 'Please fill address.')
#             return render(request, "user/register.html")
#         elif not password:
#             messages.error(request, 'Please fill password.')
#             return render(request, "user/register.html")
#         elif len(password) < 6:
#             messages.error(request, 'Password must greater than 6 character')
#             return render(request, "user/register.html")

#         try:
#             # it check username is already taken or not
#             if User.objects.filter(username = username).first():
#                 messages.success(request, 'Username is taken.')
#                 return render(request, "user/register.html")

#             # it check email is already taken or not
#             if User.objects.filter(email = email).first():
#                 messages.success(request, 'Email is taken.')
#                 return render(request, "user/register.html")
            
#             # creating user
#             user_obj = User(username = username , email = email)
#             user_obj.set_password(password)
#             user_obj.save()
#             auth_token = str(uuid.uuid4())
#             print('this is user obj')
#             # creating profile of user
#             profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token , address=address)
#             profile_obj.save()
#             print('this is profile obj')
#             # send mail to user for authenticate 
#             send_mail_after_registration(email , auth_token)
#             messages.success(request, 'Email sended to user plese check.')
#             return redirect("/login")

#         except Exception as e:
#             print(e)

# # it send email to user with token
# def send_mail_after_registration(email , token):
#     subject = 'Your accounts need to be verified'
#     message = f'Hi paste the link to verify your account http://localhost:8000/verify/{token}'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message , email_from ,recipient_list )
