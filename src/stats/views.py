from rest_framework import mixins, viewsets

from .models import ProductHistory, ProductTracking
from .serializers import ProductHistorySerializer, ProductTrackingSerializer


class ProductTrackingViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    queryset = ProductTracking.objects.all().select_related("user")
    serializer_class = ProductTrackingSerializer

    def get_queryset(self):
        return ProductTracking.objects.filter(user=self.request.user)


class ProductHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductHistory.objects.all()
    serializer_class = ProductHistorySerializer
