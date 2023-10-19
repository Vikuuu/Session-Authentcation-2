from django.urls import path
from .views import getCSRFToken, signupView

urlpatterns = [
    path("csrf_cookie", getCSRFToken.as_view()),
    path("register", signupView.as_view()),
]
