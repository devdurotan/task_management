import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import UserMaster, Role
from tasks.models import Task


# ---------- Comman For Reuse ----------

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def roles(db):
    admin_role = Role.objects.create(name="Admin")
    user_role = Role.objects.create(name="User")
    return admin_role, user_role


@pytest.fixture
def user(db, roles):
    _, user_role = roles
    return UserMaster.objects.create_user(
        email="user@test.com",
        full_name="Normal User",
        password="Test@1234",
        role=user_role,
    )


@pytest.fixture
def admin(db, roles):
    admin_role, _ = roles
    return UserMaster.objects.create_user(
        email="admin@test.com",
        full_name="Admin User",
        password="Test@1234",
        role=admin_role,
    )


@pytest.fixture
def auth_client_user(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def auth_client_admin(api_client, admin):
    api_client.force_authenticate(user=admin)
    return api_client


@pytest.fixture
def task(user):
    return Task.objects.create(
        title="Sample Task",
        description="Test description",
        completed=False,
        created_by=user,
    )


# ---------- TASK VIEWSET (USER) ----------

@pytest.mark.django_db
def test_create_task_success(auth_client_user):
    url = reverse("tasks_management-list")

    payload = {
        "title": "New Task",
        "description": "Something",
        "completed": False,
    }

    response = auth_client_user.post(url, payload, format="json")

    assert response.status_code == 201
    assert response.data["data"]["title"] == "New Task"


@pytest.mark.django_db
def test_create_task_validation_error(auth_client_user):
    url = reverse("tasks_management-list")

    response = auth_client_user.post(url, {}, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_list_tasks_only_user_tasks(auth_client_user, user):
    Task.objects.create(title="Task1", created_by=user)
    Task.objects.create(title="Task2", created_by=user)

    url = reverse("tasks_management-list")
    response = auth_client_user.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 2  # paginated response


@pytest.mark.django_db
def test_retrieve_task(auth_client_user, task):
    url = reverse("tasks_management-detail", args=[task.id])
    response = auth_client_user.get(url)

    assert response.status_code == 200
    assert response.data["data"]["id"] == task.id


@pytest.mark.django_db
def test_update_task(auth_client_user, task):
    url = reverse("tasks_management-detail", args=[task.id])

    response = auth_client_user.put(
        url,
        {"title": "Updated Task", "description": "Updated", "completed": True},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["data"]["title"] == "Updated Task"


@pytest.mark.django_db
def test_delete_task(auth_client_user, task):
    url = reverse("tasks_management-detail", args=[task.id])

    response = auth_client_user.delete(url)

    assert response.status_code == 200
    assert Task.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_access_others_task(auth_client_user, roles):
    _, user_role = roles

    other_user = UserMaster.objects.create_user(
        email="other@test.com",
        full_name="Other User",
        password="Test@1234",
        role=user_role,
    )

    task = Task.objects.create(title="Other Task", created_by=other_user)

    url = reverse("tasks_management-detail", args=[task.id])
    response = auth_client_user.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_filter_tasks(auth_client_user, user):
    Task.objects.create(title="Done Task", completed=True, created_by=user)
    Task.objects.create(title="Pending Task", completed=False, created_by=user)

    url = reverse("tasks_management-list") + "?completed=true"
    response = auth_client_user.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_search_tasks(auth_client_user, user):
    Task.objects.create(title="Buy milk", created_by=user)
    Task.objects.create(title="Read book", created_by=user)

    url = reverse("tasks_management-list") + "?search=milk"
    response = auth_client_user.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_task_requires_authentication(api_client):
    url = reverse("tasks_management-list")
    response = api_client.get(url)

    assert response.status_code == 401


# ---------- ADMIN VIEWSET ----------

@pytest.mark.django_db
def test_admin_can_list_all_tasks(auth_client_admin, user):
    Task.objects.create(title="Task1", created_by=user)
    Task.objects.create(title="Task2", created_by=user)

    url = reverse("task_list_admin-list")
    response = auth_client_admin.get(url)

    assert response.status_code == 200
    assert response.data["count"] == 2


@pytest.mark.django_db
def test_user_cannot_access_admin_endpoint(auth_client_user):
    url = reverse("task_list_admin-list")
    response = auth_client_user.get(url)

    assert response.status_code == 403