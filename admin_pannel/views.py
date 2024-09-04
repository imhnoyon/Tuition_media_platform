from django.shortcuts import render
from .models import AdminModel
from .serializers import UserSerializer,AdminSerializer,AdminRegistrationSerializer,AdminLoginSerializer
# Create your views here.
from rest_framework import viewsets,status
from django.contrib.auth.models import User
#for sending email modules
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

# registration and login modules
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout

# class AdminApiView(APIView):
#     queryset=AdminModel.objects.all()
#     serializer_class=AdminSerializer


class AdminApiView(APIView):
    def get(self, request, format=None):
        snippets = AdminModel.objects.all()
        serializer = AdminSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class adminFilterViewset(APIView):
#     def get(self, request, format=None):
#         snippets = AdminModel.objects.get(user=request.user)
#         serializer = AdminSerializer(snippets, many=False)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = AdminSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRegistrationView(APIView):
    serializer_class=AdminRegistrationSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            admin=serializer.save()
            token=default_token_generator.make_token(admin)
            uid=urlsafe_base64_encode(force_bytes(admin.pk))

            confrim_link=f"http://127.0.0.1:8000/adminpannel/active/{uid}/{token}"
            email_subject="Confirm Registration"
            email_body=render_to_string('confirm_email.html',{'confirm_link':confrim_link})
            email=EmailMultiAlternatives(email_subject,'',to=[admin.email])
            email.attach_alternative(email_body,'text/html')
            email.send()

            return Response("Check email for confirmation")
        return Response(serializer.errors)
    


def activateView(request,uid64,token):
    try:
        print("Inside try")
        uid=urlsafe_base64_decode(uid64).decode()
        admin=User._default_manager.get(pk=uid)
        
    except(User.DoesNotExist):
        admin=None
        
    if admin is not None and default_token_generator.check_token(admin,token):
        admin.is_active=True 
        admin.save()
        print("admin save")
        return redirect('login')
    else:
        return redirect('register')





class AdminLoginApiView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=self.request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
           
            admin = authenticate(username=username, password=password)
            
            if admin:
                try:               
                    admin_data = AdminModel.objects.get(user=admin)
                    admin_id = admin_data.id                
                    token,_=Token.objects.get_or_create(user=admin)
                    login(request, admin) 
                    
                    return Response({'Token': token.key, 'admin_id': admin_id})
                except AdminModel.DoesNotExist:
                    return Response({'error': "admin data not found"})
            else:
                return Response({'error': "Invalid credentials"})
        return Response(serializer.errors)
    


class AdminLogoutApiView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
            logout(request)
            return redirect('login')
        else:
            return Response({'message': 'You are not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)