from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, AppointmentView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api')


urlpatterns = [
    path('', include(router.urls)),
    path('appointment/', AppointmentView.as_view(), name='appointment')
]
