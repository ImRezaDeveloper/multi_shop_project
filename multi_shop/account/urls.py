from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('check-otp/', views.CheckOtpView.as_view(), name='check_otp'),
    
]
