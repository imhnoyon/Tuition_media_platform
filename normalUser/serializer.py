from rest_framework import serializers
from .models import Student
from django.contrib.auth.models import User
from .models import Student
from .constrains import GENDER_CHOICES

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']



class StudentRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)
    gender = serializers.CharField(max_length=10, required=True)
    mobile = serializers.CharField(max_length=15, required=True)
    location = serializers.CharField(max_length=100, required=True)
    tuition_district = serializers.CharField(max_length=100, required=True)
    minimum_salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    status = serializers.CharField(max_length=20, required=False, allow_blank=True)
    days_per_week = serializers.IntegerField(default=5)
    tutoring_experience = serializers.CharField(max_length=20, required=True)
    medium_of_instruction = serializers.CharField(max_length=20, required=True)
   
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password',
                  'image', 'gender', 'mobile', 'location', 'tuition_district', 'minimum_salary',
                  'status', 'days_per_week', 'tutoring_experience',
                  'medium_of_instruction']
        
    def save(self):
        username=self.validated_data['username']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        email=self.validated_data['email']
        password=self.validated_data['password']
        confirm_password=self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'error': "Password Doesn't Match"})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email Already Exists"})
        
        account = User(username=username, first_name=first_name, last_name=last_name, email=email)
        account.set_password(password)
        account.is_active = False  # User needs verification
        account.save()


        tutor = Student.objects.create(
            user=account,
            image=self.validated_data['image'],
            gender=self.validated_data['gender'],
            mobile=self.validated_data['mobile'],
            location=self.validated_data['location'],
            tuition_district=self.validated_data['tuition_district'],
            minimum_salary=self.validated_data.get('minimum_salary'),
            status=self.validated_data.get('status', 'Available'),
            tutoring_experience=self.validated_data['tutoring_experience'],
            medium_of_instruction=self.validated_data['medium_of_instruction'],
           
        )
        return account

class TutorLoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)    

    class Meta:
        model=User
        fields=['username','password']



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "New passwords do not match."})
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


    