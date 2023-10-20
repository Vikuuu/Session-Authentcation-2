from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib import auth
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from user_profile.models import UserProfile
from .serializer import UserAccountSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@method_decorator(ensure_csrf_cookie, name="dispatch")
class getCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        try:
            return Response({"success": "CSRF cookie set"})
        except:
            return Response({"error": "Something went wrong"})


@method_decorator(csrf_protect, name="dispatch")
class signupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        email = data["email"]
        username = data["username"]
        password = data["password"]
        re_password = data["re_password"]

        try:
            if password == re_password:
                if User.objects.filter(username=username).exists():
                    return Response({"error": "Username already exists"})
                else:
                    if User.objects.filter(email=email).exists():
                        return Response({"error": "Email already exists"})
                    else:
                        if len(password) < 6:
                            return Response({"error": "Password should greater than 6"})
                        else:
                            user = User.objects.create_user(email, username, password)
                            user.save()
                            user = User.objects.get(id=user.id)

                            user_profile = UserProfile.objects.create(user=user)
                            user_profile.save()

                            return Response({"success": "User created successfully"})
            else:
                return Response({"error": "Passwords does not match"})
        except Exception as e:
            return Response({"error": "Something went wrong !!!  " + str(e)})


@method_decorator(csrf_protect, name="dispatch")
class loginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data

        email = data["email"]
        password = data["password"]

        try:
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return Response({"success": "User logged in successfully"})
            else:
                return Response({"error": "User not available"})
        except Exception as e:
            return Response(
                {"error": "Something went wrong while logging in  " + str(e)}
            )

class logoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({"success" : "User logged out successfully"})
        except Exception as e:
            return Response({"error" : "Something went wrong while logging out  " + str(e)})