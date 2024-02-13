from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView


urlpatterns = [
    path("", views.login_page, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("password-reset-view/", views.CustomPasswordResetView.as_view()),
    path("password-reset-done/", PasswordResetDoneView.as_view()),
    path(
        "password-tiklash/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
    ),
    path("password-reset-complete/", PasswordResetCompleteView.as_view()),
    # profile
]
