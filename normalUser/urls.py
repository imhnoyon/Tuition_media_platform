from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewset,ClassFilter,StudentRegistrationView,activate,StudentLoginApiView,StudentLogoutApiView,ChangePasswordApiView,StudentFilterViewset

# router=DefaultRouter()

# router.register('list',StudentViewset)


urlpatterns = [
    # path('', include(router.urls)),
    path('list/',StudentViewset.as_view()),
    path('filterstudent/',StudentFilterViewset.as_view()),
    path('classfilter/',ClassFilter.as_view()),
    path("register/", StudentRegistrationView.as_view(), name="student_register"),
    path("login/", StudentLoginApiView.as_view(), name="student_login"),
    path('logout/',StudentLogoutApiView.as_view(),name='student_logout'),
    path("active/<uid64>/<token>/",activate,name='activate'),
    path('change-password/', ChangePasswordApiView.as_view(), name='change-password'),
]