from django.urls import path
from . import views

urlpatterns = [
    path('join/', views.join, name='join'),
    path('success/', views.success, name='success'),
    path('login/', views.LoginView.as_view(), name='login'),
]
