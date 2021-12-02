from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView




# for logout


class Logout(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        return Response({"status":"user logged out"}, status=status.HTTP_200_OK)



# def logout(req):
#     auth.logout(req)
#     return Response({"status":"User succesfully logged out"}, status=status.HTTP_200_OK)