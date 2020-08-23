from django.urls import path
from account.api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('account/register/', views.registration_view),
    path('account/login/', views.CustomAuthToken.as_view()),
    path('account/', views.AccountList.as_view()),
    path('account/<int:pk>/', views.AccountDetail.as_view())
]