from django.urls import include, path
from rest_framework.routers import SimpleRouter

from stats.views import ProductHistoryViewSet, ProductTrackingViewSet

trackings_router = SimpleRouter()
trackings_router.register(r'trackings', ProductTrackingViewSet, basename='trackings')

history_router = SimpleRouter()
history_router.register(r'product-states', ProductHistoryViewSet, basename='product-states')


urlpatterns = [
    path('', include(trackings_router.urls)),
    path('', include(history_router.urls)),
]