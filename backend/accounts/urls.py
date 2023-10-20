from django.urls import path
from .views import getCSRFToken, signupView, loginView, logoutView

urlpatterns = [
    path("csrf_cookie", getCSRFToken.as_view()),
    path("register", signupView.as_view()),
    path("login", loginView.as_view()),
    path("logout", logoutView.as_view()),
]
