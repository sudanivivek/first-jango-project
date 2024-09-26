from django.urls import path
# from .views import edit_profile/
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
    # path('edit-profile/', edit_profile, name='edit_profile'),   
    
]
    # path('', views.register, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('profile/', views.profile, name='profile'),
    # path('logout/', views.logout_view, name='logout'),
    # path('password-reset/', views.password_reset_request, name='password_reset_request'),
    # path('password-reset/confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
