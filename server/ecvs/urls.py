from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CredentialViewSet, WalletView
from ecvs.views import UserViewSet, CredentialViewSet, register_user
from django.contrib import admin

router = DefaultRouter()
router.register(r'credentials', CredentialViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', register_user, name='register'),
    path('wallet/', WalletView.as_view(), name='wallet'),
]
