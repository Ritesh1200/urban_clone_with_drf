from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from rest_framework import status
from rest_framework.response import Response
from ..serializers import CategorySerializer, EmployeeSerializer
from rest_framework.views import APIView
from user.models import Profile , Services , Categorys , Employee , Choose 
from django.contrib.auth.decorators import login_required

class Category(APIView):
    def get(self , request , pk):
        if request.user.is_authenticated:
            user_obj = request.user
            profile_obj = Profile.objects.filter(user = user_obj).first()
            if profile_obj is None:
                return Response({"error":"Please not login with admin account"}, status.HTTP_400_BAD_REQUEST)


        ser_obj = Services.objects.filter(pk = pk).first()

        # if any sercice have sub category to redirect to category otherwise service
        if not ser_obj.sub_category:
            return Response({"error":"No category for this service"}, status.HTTP_400_BAD_REQUEST)
        
        cat_obj = Categorys.objects.filter(service = ser_obj.service)
        serializer = CategorySerializer(cat_obj , many = True) 

        return Response(serializer.data , status= status.HTTP_200_OK)

class Service(APIView):
    def get(self , request ,servicepk, categorypk = None):
        if request.user.is_authenticated:
            user_obj = request.user
            profile_obj = Profile.objects.filter(user = user_obj).first()
            if profile_obj is None:
                return Response({"error":"Please not login with admin account"}, status.HTTP_400_BAD_REQUEST)


            # it check there is sub category or not
            ser_obj = Services.objects.filter(pk = servicepk).first()
            if categorypk is None:
                emp_obj = Employee.objects.filter(service = ser_obj.service).all()
                empserializer = EmployeeSerializer(emp_obj , many = True)
                print(emp_obj)
                cat = ser_obj.service
            else:
                cat_obj = Categorys.objects.filter(pk = categorypk).first()
                emp_obj = Employee.objects.filter(category = cat_obj.category).all()
                empserializer = EmployeeSerializer(emp_obj , many = True)
                cat = cat_obj.category

            emplist = []
            for emp in emp_obj:
                emp_data = Employee.objects.filter(pk = emp.id).first()
                choose_obj = Choose.objects.filter(emp_id = emp.id, cart=True).first()
                gotocart = False
                if choose_obj:
                    gotocart = True


                # it add all data to list
                Disc={"name":emp_data.name,"image":emp_data.image,"description":emp_data.description,"cost":emp_data.cost,"rating":emp_data.rating , "address":emp_data.address,"id":emp_data.id, "gotocart":gotocart}

                emplist.append(Disc)

            
            return Response(empserializer.data , status=status.HTTP_200_OK)



# def category(req, pk):

#     # it check user login with admin account 
#     if req.user.is_authenticated:
#         user_obj = req.user
#         profile_obj = Profile.objects.filter(user = user_obj).first()
#         if profile_obj is None:
#             return redirect('/login')

    
#     ser_obj = Services.objects.filter(pk = pk).first()

#     # if any sercice have sub category to redirect to category otherwise service
#     if not ser_obj.sub_category:
#         return redirect(f'/service/{ser_obj.id}')
    
#     cat_obj = Categorys.objects.filter(service = ser_obj.service)

#     return render(req , 'user/category.html' , {"categorys":cat_obj , 'serviceid': ser_obj.id})

        
        
# def service(req ,servicepk, categorypk = None):

#     # it check user login with admin account 
#     if req.user.is_authenticated:
#         user_obj = req.user
#         profile_obj = Profile.objects.filter(user = user_obj).first()
#         if profile_obj is None:
#             return redirect('/login')

#     # it check there is sub category or not
#     ser_obj = Services.objects.filter(pk = servicepk).first()
#     if categorypk is None:
#         emp_obj = Employee.objects.filter(service = ser_obj.service).all()
#         cat = ser_obj.service
#     else:
#         cat_obj = Categorys.objects.filter(pk = categorypk).first()
#         emp_obj = Employee.objects.filter(category = cat_obj.category).all()
#         cat = cat_obj.category

#     emplist = []
#     for emp in emp_obj:
#         emp_data = Employee.objects.filter(pk = emp.id).first()
#         choose_obj = Choose.objects.filter(emp_id = emp.id, cart=True).first()
#         gotocart = False
#         if choose_obj:
#             gotocart = True


#         # it add all data to list
#         Disc={"name":emp_data.name,"image":emp_data.image,"description":emp_data.description,"cost":emp_data.cost,"rating":emp_data.rating , "address":emp_data.address,"id":emp_data.id, "gotocart":gotocart}

#         emplist.append(Disc)

#     return render(req , 'user/service.html' , {'emp_present': len(emplist) ,'cat': cat,  'employees' : emplist , 'servicepk':servicepk , 'categorypk' : categorypk})
