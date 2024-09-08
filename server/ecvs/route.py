from django.urls import path
from .views import create_credential, credential_list, verify_credential

urlpatterns = [
    path('create/', create_credential, name='create_credential'),
    path('list/', credential_list, name='credential_list'),
    path('verify/<str:credential_id>/', verify_credential, name='verify_credential'),
]
