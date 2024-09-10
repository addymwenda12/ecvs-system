from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CredentialViewSet, WalletView, UserViewSet
from ecvs.views import register_user
from django.contrib import admin

router = DefaultRouter()
router.register(r'credentials', CredentialViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', register_user, name='register'),
    path('api/login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('wallet/', WalletView.as_view(), name='wallet'),
]
