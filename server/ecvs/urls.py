from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CredentialViewSet, WalletView

router = DefaultRouter()
router.register(r'credentials', CredentialViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('wallet/', WalletView.as_view(), name='wallet'),
]
