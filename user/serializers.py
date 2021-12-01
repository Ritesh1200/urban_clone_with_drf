from rest_framework import serializers
from user.models import Services , Profile , Categorys , Employee , Choose
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User



class ServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = "__all__"  


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password','email')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"  

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorys
        fields = "__all__"  

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"  


class ChooseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choose
        fields = "__all__"  


