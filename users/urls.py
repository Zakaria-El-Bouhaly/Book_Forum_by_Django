from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("Register", views.Register, name="Register"),
    path("Profile", views.Profile, name="Profile"),
    path(
        "Login/",
        auth_views.LoginView.as_view(
            template_name="users/Login.html", redirect_authenticated_user=True
        ),
        name="Login",
    ),
    path(
        "Logout/",
        auth_views.LogoutView.as_view(template_name="users/Logout.html"),
        name="Logout",
    ),
    path(
        "password-reset",
        auth_views.PasswordResetView.as_view(template_name="users/pass_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/pass_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/pass_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/pass_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
