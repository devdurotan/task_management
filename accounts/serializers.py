from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from .models import UserMaster


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserMaster
        fields = ("email", "full_name", "password", "confirm_password")

    def validate_email(self, value):
        if UserMaster.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value.lower()

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        validate_password(attrs["password"])
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")

        user = UserMaster.objects.create_user(**validated_data)
        user.set_password(password)
        user.role_id = 2
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = UserMaster.objects.get(email=email)
        except UserMaster.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        attrs["user"] = user
        return attrs
    

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password")

        # 🔹 Check user exists (case-insensitive)
        user = UserMaster.objects.filter(email__iexact=email).select_related("role").first()
        if not user:
            raise serializers.ValidationError("Invalid email")

        # 🔹 Check password
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        # remove this if serializer is used for normal login
        if user.role and user.role.name != "Admin":
            raise serializers.ValidationError({"detail": "You are not authorized as admin"})

        attrs["user"] = user
        return attrs