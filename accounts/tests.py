import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import UserMaster, Role

@pytest.fixture
def api_client():
    return APIClient()


# Registration Success Tests
@pytest.mark.django_db
def test_user_registration_success(api_client):
    # create role with id=2 (User role)
    Role.objects.create(id=2, name="User")

    url = reverse("users_registration-list")

    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "StrongPass@123",
        "confirm_password": "StrongPass@123",
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201

# Registration Failure Tests
# Registration with password missmatch
@pytest.mark.django_db
def test_user_registration_password_mismatch(api_client):
    url = reverse("users_registration-list")

    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "StrongPass@123",
        "confirm_password": "WrongPass@123",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "password" in str(response.data["errors"])


# Registration with Duplicate Email
@pytest.mark.django_db
def test_user_registration_duplicate_email(api_client):
    UserMaster.objects.create_user(email="test@example.com", full_name="Existing")

    url = reverse("users_registration-list")

    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "StrongPass@123",
        "confirm_password": "StrongPass@123",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400


# Get Registered User List Tests    
@pytest.mark.django_db
def test_user_registration_get_list(api_client):
    role = Role.objects.create(id=2, name="User")

    # create sample users
    UserMaster.objects.create_user(
        email="user1@example.com",
        full_name="User One",
        password="Test@1234",
        role=role,
    )

    UserMaster.objects.create_user(
        email="user2@example.com",
        full_name="User Two",
        password="Test@1234",
        role=role,
    )

    url = reverse("users_registration-list")

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["email"] == "user1@example.com"
    assert response.data[1]["email"] == "user2@example.com"

# Get Registered User by ID Tests
@pytest.mark.django_db
def test_user_registration_get_by_id(api_client):
    role = Role.objects.create(id=2, name="User")

    user = UserMaster.objects.create_user(
        email="testget@example.com",
        full_name="Test Get",
        password="Test@1234",
        role=role,
    )

    url = reverse("users_registration-detail", args=[user.id])

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["email"] == user.email
    assert response.data["full_name"] == user.full_name


# User Login Tests
# Login Success Tests
@pytest.mark.django_db
def test_login_success(api_client):
    role = Role.objects.create(id=2, name="User")
    user = UserMaster.objects.create_user(email="login@example.com", full_name="Login User", password="Test@1234", role=role)

    url = reverse("users_login-list")

    payload = {
        "email": "login@example.com",
        "password": "Test@1234",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 200
    assert "access_token" in response.data["data"]
    assert response.data["data"]["user"]["email"] == user.email

# Login Failiurre with invalid password test
@pytest.mark.django_db
def test_login_invalid_password(api_client):
    role = Role.objects.create(id=2, name="User")
    user = UserMaster.objects.create_user(email="login@example.com", full_name="Login User", password="Test@1234", role=role)

    url = reverse("users_login-list")

    payload = {
        "email": "login@example.com",
        "password": "Test@7787878",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400

# Login Failure with invalid email test
@pytest.mark.django_db
def test_login_invalid_email(api_client):
    role = Role.objects.create(id=2, name="User")
    user = UserMaster.objects.create_user(email="login@example.com", full_name="Login User", password="Test@1234", role=role)

    url = reverse("users_login-list")

    payload = {
        "email": "login123@example.com",
        "password": "Test@7787878",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400



# ADMIN Login Tests
# Login Success Tests
@pytest.mark.django_db
def test_admin_login_success(api_client):
    role = Role.objects.create(id=1, name="Admin")
    user = UserMaster.objects.create_user(email="admin@example.com", full_name="Admin User", password="Test@1234", role=role)

    url = reverse("admin_login-list")

    payload = {
        "email": "admin@example.com",
        "password": "Test@1234",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 200
    assert "access_token" in response.data["data"]
    assert response.data["data"]["user"]["email"] == user.email

# Login Failure with invalid password test
@pytest.mark.django_db
def test_admin_login_invalid_password(api_client):
    role = Role.objects.create(id=1, name="Admin")
    user = UserMaster.objects.create_user(email="admin@example.com", full_name="Admin User", password="Test@1234", role=role)

    url = reverse("admin_login-list")

    payload = {
        "email": "admin@example.com",
        "password": "Test@4321",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400

# Login Failure with invalid email test
@pytest.mark.django_db
def test_admin_login_invalid_email(api_client):
    role = Role.objects.create(id=1, name="Admin")
    user = UserMaster.objects.create_user(email="admin@example.com", full_name="Admin User", password="Test@1234", role=role)

    url = reverse("admin_login-list")

    payload = {
        "email": "admin123@example.com",
        "password": "Test@4321",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400

    payload = {
        "email": "admin@example.com",
        "password": "Test@4321",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400


# Login Faliure with non-admin user test
@pytest.mark.django_db
def test_admin_login_falure_with_non_admin_user(api_client):
    role = Role.objects.create(id=2, name="User")
    user = UserMaster.objects.create_user(email="admin@example.com", full_name="Admin User", password="Test@1234", role=role)

    url = reverse("admin_login-list")

    payload = {
        "email": "admin@example.com",
        "password": "Test@1234",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400