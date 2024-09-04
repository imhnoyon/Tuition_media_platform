from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import AdminApiView,AdminLoginApiView,AdminLogoutApiView,AdminRegistrationView,activateView



urlpatterns = [
    
    path('list/',AdminApiView.as_view()),
    # path('adminfilter/',adminFilterViewset.as_view()),
    path("register/", AdminRegistrationView.as_view(), name="register"),
    path("login/", AdminLoginApiView.as_view(), name="login"),
    path('logout/',AdminLogoutApiView.as_view(),name='logout'),
    path("active/<uid64>/<token>/",activateView,name='activate'),
]


