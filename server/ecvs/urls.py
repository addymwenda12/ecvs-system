from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CredentialViewSet, WalletViewSet, UserViewSet
from ecvs.views import register_user

router = DefaultRouter()
router.register(r'credentials', CredentialViewSet)
router.register(r'users', UserViewSet)
router.register(r'wallet', WalletViewSet, basename='wallet')

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('', include(router.urls)),
]
