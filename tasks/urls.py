from rest_framework.routers import DefaultRouter
from .views import AdminDataViewSet, TaskViewSet

router = DefaultRouter()
router.register("tasks_management", TaskViewSet, basename="tasks_management")
router.register("task_list_admin", AdminDataViewSet, basename="task_list_admin")


urlpatterns = router.urls