from user.models import Services 
from .serializers import ServicesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# home page

class Home(APIView):
    def get(self , request):
        services = Services.objects.all()
        serializer = ServicesSerializer(services ,  many=True , context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



# def home(req):
#     services = Services.objects.all()
#     serializer = ServicesSerializer(services ,  many=True , context={'request': req})
#     return render(req, 'user/home.html' , {"services" : serializer.data})


