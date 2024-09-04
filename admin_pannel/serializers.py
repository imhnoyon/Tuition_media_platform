from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AdminModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username', 'first_name', 'last_name', 'email']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminModel
        fields=['id','mobile_no','user']



class AdminRegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True)
    mobile_no=serializers.CharField(max_length=12)

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','mobile_no','password','confirm_password']

    def save(self):
        username=self.validated_data['username']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        email=self.validated_data['email']
        mobile_no=self.validated_data['mobile_no']
        password=self.validated_data['password']
        confirm_password=self.validated_data['confirm_password']

        if password!=confirm_password:
            raise serializers.ValidationError({'error' : "Password Doesn't Matched"}) #raising error
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already Exists"})
        

        
        account=User(username=username,first_name=first_name,last_name=last_name,email=email)
        account.set_password(password)
        account.is_active=False
        account.save()

        admin = AdminModel.objects.create(user=account, mobile_no=mobile_no)
        return account
    

class AdminLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

    class Meta:
        model=AdminModel
        fields=['username','password']
        
