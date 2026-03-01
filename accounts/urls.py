from rest_framework.routers import DefaultRouter
from accounts.views import AdminLoginViewSet, LoginViewSet, UserRegistrationViewSet

router = DefaultRouter()
router.register("users_registration", UserRegistrationViewSet, basename="users_registration")
router.register("users_login", LoginViewSet, basename="users_login")
router.register("admin_login", AdminLoginViewSet, basename="admin_login")

urlpatterns = router.urls