from django.urls import path
from .views import register, login,dashboard
from .views import profile,logout,update
from django.urls import path


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard,name='dashboard'),
    path('profile',profile,name='profile'),
    path('logout/', logout, name='logout'),
    path('update/',update,name='update'),
]