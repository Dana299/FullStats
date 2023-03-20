from django.urls import include, path
from rest_framework.routers import SimpleRouter
from stats.views import ProductTrackingViewSet

router = SimpleRouter()
router.register(r'trackings', ProductTrackingViewSet)


urlpatterns = [
    path('', include(router.urls))
]