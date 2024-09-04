from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewset
router = DefaultRouter()

router.register('application',ApplicationViewset)

urlpatterns = [
    path('teacher/', include(router.urls)),
]