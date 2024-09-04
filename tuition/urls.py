from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TuitionViewset,ReviewViewset,TuitionDetail

# router=DefaultRouter()

# router.register('tuitionlist',TuitionViewset)
# router.register('review',ReviewViewset)

urlpatterns = [
    # path('', include(router.urls)),
    path('review/',ReviewViewset.as_view()),
    path('tuitionlist/',TuitionViewset.as_view()),
    path("details/<int:pk>/", TuitionDetail.as_view(), name="tuition_detail"),
]