from django.urls import path
from . import views
from Mission_Book import settings
from django.conf.urls.static import static

urlpatterns = [
    path('join/', views.join, name='join'),
    path('success/', views.success, name='success'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/',views.profile, name='profile'),
    path('change_profile/',views.change_profile, name='change_profile'),
    path('change_name/',views.change_name,name='change_name'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
