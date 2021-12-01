from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView




# for logout


class Logout(APIView):

    def get(self, request):
        auth.logout(request)
        return Response({"status":"user logged out"}, status=status.HTTP_200_OK)



# def logout(req):
#     auth.logout(req)
#     return Response({"status":"User succesfully logged out"}, status=status.HTTP_200_OK)