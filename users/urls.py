from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('Register', views.Register, name="Register"),
    path('Profile', views.Profile, name="Profile"),
    path('Login/', auth_views.LoginView.as_view(template_name='users/Login.html',redirect_authenticated_user=True), name='Login'),
    path('Logout/', auth_views.LogoutView.as_view(template_name='users/Logout.html'), name='Logout'),
]
