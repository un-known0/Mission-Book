from django.urls import path
from . import views
from Mission_Book import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index_null, name='index_null'),
    path('index/<int:category>',views.index, name='index'),
    path('join/', views.join, name='join'),
    path('prolog/<int:num>',views.prolog, name='prolog'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_member, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('mypage/',views.mypage, name='mypage'),
    path('setup/',views.setup, name='setup'),
    path('select_title/',views.select_title, name='select_title'),
    path('change_title/<int:title>/',views.change_title, name='change_title'),
    path('change_title_color/<int:color>/',views.change_title_color, name='change_title_color'),
    path('ending/<int:num>',views.ending, name='ending'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
