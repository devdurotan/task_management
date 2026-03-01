from rest_framework import viewsets, permissions, status
from django.db import transaction

from accounts.models import Role
from task_manager.pagination import CustomPagination
from .models import Task
from .serializers import TaskSerializer
from task_manager.response import APIResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from task_manager.permissions import IsRoleAdmin, IsRoleUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsRoleUser]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["completed"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return Task.objects.none()
        return Task.objects.filter(created_by=user)
    
    @swagger_auto_schema(
    operation_summary="Create a new task",
    security=[{"Bearer": []}],
    request_body=TaskSerializer,
    responses={
        201: openapi.Response(
            description="Task created successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Task created successfully"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            "title": openapi.Schema(type=openapi.TYPE_STRING, example="Finish docs"),
                            "description": openapi.Schema(type=openapi.TYPE_STRING, example="Write swagger docs"),
                            "completed": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                            "created_by": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                        },
                    ),
                },
            ),
        )
    },)
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return APIResponse.bad_request(
                message="Validation failed",
                errors=serializer.errors
            )

        serializer.save(created_by=request.user)

        return APIResponse.created(
            message="Task created successfully",
            data=serializer.data
        )
    @swagger_auto_schema(
    operation_summary="Get all tasks of logged-in user",
    security=[{"Bearer": []}],
    responses={
        200: openapi.Response(
            description="Tasks fetched successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Tasks fetched successfully"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                                "title": openapi.Schema(type=openapi.TYPE_STRING, example="Finish docs"),
                                "description": openapi.Schema(type=openapi.TYPE_STRING),
                                "completed": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                "created_by": openapi.Schema(type=openapi.TYPE_INTEGER),
                            },
                        ),
                    ),
                },
            ),
        )
    },
)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return APIResponse.success(
            message="Tasks fetched successfully",
            data=serializer.data
        )
    @swagger_auto_schema(
    operation_summary="Get task details",
    security=[{"Bearer": []}],
    responses={
        200: openapi.Response(
            description="Task retrieved successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Task retrieved successfully"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                            "title": openapi.Schema(type=openapi.TYPE_STRING),
                            "description": openapi.Schema(type=openapi.TYPE_STRING),
                            "completed": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            "created_by": openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                },
            ),
        )
    },
)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return APIResponse.success(
            message="Task retrieved successfully",
            data=serializer.data
        )
    @swagger_auto_schema(
    operation_summary="Update task",
    security=[{"Bearer": []}],
    request_body=TaskSerializer,
    responses={
        200: openapi.Response(
            description="Task updated successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Task updated successfully"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                            "title": openapi.Schema(type=openapi.TYPE_STRING),
                            "description": openapi.Schema(type=openapi.TYPE_STRING),
                            "completed": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            "created_by": openapi.Schema(type=openapi.TYPE_INTEGER),
                        },
                    ),
                },
            ),
        )
    },
)
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if not serializer.is_valid():
            return APIResponse.bad_request(
                message="Validation failed",
                errors=serializer.errors
            )

        serializer.save()

        return APIResponse.success(
            message="Task updated successfully",
            data=serializer.data
        )
    @swagger_auto_schema(
    operation_summary="Delete task",
    security=[{"Bearer": []}],
    responses={
        200: openapi.Response(
            description="Task deleted successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Task deleted successfully"),
                },
            ),
        )
    },
)
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return APIResponse.success(message="Task deleted successfully")
    




class AdminDataViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsRoleAdmin]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["completed"]
    search_fields = ["title", "description"]
    http_method_names = ["get"]