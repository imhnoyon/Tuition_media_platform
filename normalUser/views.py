from django.shortcuts import render
from rest_framework import viewsets,generics,status,filters
from rest_framework import viewsets
from .models import Student
from rest_framework.authtoken.models import Token
from .serializer import StudentSerializer
from rest_framework import generics
from tuition.models import Tuition
from tuition.serializer import TuitionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from .serializer import StudentRegistrationSerializer,TutorLoginSerializer,ChangePasswordSerializer
# registration and login modules
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.response import Response
#for sending email modules
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView

# class TeacherViewset(viewsets.ModelViewSet):
# class StudentViewset(APIView):
#     queryset=Student.objects.all()
#     serializer_class=StudentSerializer

class StudentFilterViewset(APIView):
    def get(self, request, format=None):
        snippets = Student.objects.get(user=request.user)
        serializer = StudentSerializer(snippets, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentViewset(APIView):
    def get(self, request, format=None):
        snippets = Student.objects.all()
        # std_obj=Student.objects.get(user=request.user)
        serializer = StudentSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassFilter(generics.ListAPIView):
    queryset = Tuition.objects.all()
    serializer_class = TuitionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tuition_class']


# Teacher registration view

class StudentRegistrationView(APIView):
    serializer_class=StudentRegistrationSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data) #user details stor in serializer
        
        if serializer.is_valid(): 
            tutor=serializer.save() # save serializer in database
            token=default_token_generator.make_token(tutor)  #generate token of tutor
            uid=urlsafe_base64_encode(force_bytes(tutor.pk)) #more specified the confirmation link
            
            confirm_link=f"http://127.0.0.1:8000/tuitor/active/{uid}/{token}" #link send for confirm
            email_subject="Confirm Registration"
            email_body=render_to_string('confirm_email.html',{'confirm_link':confirm_link})
            email=EmailMultiAlternatives(email_subject,'',to=[tutor.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
            
            return Response("Check email for confirmation")
        return Response(serializer.errors)
    


def activate(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        tutor=User._default_manager.get(pk=uid)
        
    except(User.DoesNotExist):
        tutor=None
        
    if tutor is not None and default_token_generator.check_token(tutor,token):
        tutor.is_active=True # account active
        tutor.save()
        return redirect('tutor_login')
    else:
        return redirect('tutor_register')
    


class StudentLoginApiView(APIView):
    def post(self, request):
        serializer = TutorLoginSerializer(data=self.request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            # Check if Tutor exists in our database
            tutor = authenticate(username=username, password=password)
            
            if tutor:
                try:
                    # Get the tutor_id from the Tutor model
                    tutor_data = Student.objects.get(user=tutor)
                    tutor_id = tutor_data.id
                    
                    token, _ = Token.objects.get_or_create(user=tutor)
                    login(request, tutor)  # Log in the tutor
                    
                    return Response({'Token': token.key, 'tutor_id': tutor_id})
                except Student.DoesNotExist:
                    return Response({'error': "Tutor data not found"})
            else:
                return Response({'error': "Invalid credentials"})
        return Response(serializer.errors)
    



class StudentLogoutApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
            logout(request)
            return redirect('login')
        else:
            return Response({'message': 'You are not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)
        

class ChangePasswordApiView(APIView):
    
  def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordApiView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)    