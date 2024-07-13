from rest_framework import routers

from .views import ProfileViewSet, ConfirmationCodeView

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'confirmation_code', ConfirmationCodeView, basename='code')
urlpatterns = router.urls
