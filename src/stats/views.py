from rest_framework import mixins, viewsets

from .models import ProductHistory, ProductTracking
from .serializers import ProductHistorySerializer, ProductTrackingSerializer


class ProductTrackingViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = ProductTrackingSerializer

    def get_queryset(self):
        """
        Restricts the returned trackings to a given user from request.
        Optionally restricts the returned trackings to a given
        tracking period by filtering against a `tracking_interval`
        query parameter in the URL.
        """
        queryset = ProductTracking.objects.filter(user=self.request.user)
        tracking_interval = self.request.query_params.get('tracking_interval')
        if tracking_interval is not None:
            queryset = queryset.filter(tracking_interval=tracking_interval)
        return queryset


class ProductHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductHistorySerializer

    def get_queryset(self):
        """
        Optionally filters the returned product history records by
        'last_updated_from' and 'last_updated_to' query parameters in the URL
        """
        queryset = ProductHistory.objects.filter(product__user=self.request.user)
        from_ = self.request.query_params.get('last_updated_from')
        to_ = self.request.query_params.get('last_updated_to')
        if from_ is not None:
            queryset = queryset.filter(last_updated__gte=from_)
        if to_ is not None:
            queryset = queryset.filter(last_updated__lte=to_)
        return queryset
