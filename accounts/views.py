from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import UserMaster
from .serializers import *
from task_manager.response import APIResponse
from task_manager.jwt import JWTService
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = UserMaster.objects.all()
    serializer_class = UserRegistrationSerializer
    http_method_names = ["post", "get"]

    @swagger_auto_schema(
        operation_summary="Register a new user",
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": "User registered successfully",
                        "data": {
                            "id": 1,
                            "email": "user@example.com",
                            "full_name": "John Doe"
                        }
                    }
                }
            ),
            400: "Validation error"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.bad_request(
                message="Validation failed",
                errors=serializer.errors
            )
        serializer.save()
        return APIResponse.created(message="User registered successfully", data=serializer.data)
    

class LoginViewSet(viewsets.ModelViewSet):
    queryset = UserMaster.objects.none()
    serializer_class = LoginSerializer
    http_method_names = ["post"]

    @swagger_auto_schema(
        operation_summary="User login",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            "access_token": "eyJhbGciOiJIUzI1NiIs...",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
                            "user": {
                                "id": 1,
                                "email": "user@example.com",
                                "full_name": "John Doe"
                            }
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "Invalid email or password",
                        "errors": {
                            "email": ["Invalid email or password"]
                        }
                    }
                }
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return APIResponse.bad_request(
                message="Invalid email or password",
                errors=serializer.errors
            )

        user = serializer.validated_data["user"]
        tokens = JWTService.generate_tokens(user)

        return APIResponse.success(
            message="Login successful",
            data={
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                }
            }
        )
    


class AdminLoginViewSet(viewsets.ModelViewSet):
    queryset = UserMaster.objects.none()
    serializer_class = AdminLoginSerializer
    http_method_names = ["post"]

    @swagger_auto_schema(
        operation_summary="Admin login",
        request_body=AdminLoginSerializer,
        responses={
            200: openapi.Response(
                description="Admin login successful",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            "access_token": "eyJhbGciOiJIUzI1NiIs...",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
                            "user": {
                                "id": 1,
                                "email": "admin@example.com",
                                "full_name": "Admin User"
                            }
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "Invalid email or password",
                        "errors": {
                            "email": ["Invalid email or password"]
                        }
                    }
                }
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return APIResponse.bad_request(
                message="Invalid email or password",
                errors=serializer.errors
            )

        user = serializer.validated_data["user"]
        tokens = JWTService.generate_tokens(user)

        return APIResponse.success(
            message="Login successful",
            data={
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                }
            }
        )