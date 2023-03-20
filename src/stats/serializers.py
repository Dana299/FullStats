from datetime import timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import ProductHistory, ProductTracking


class ProductTrackingSerializer(serializers.ModelSerializer):
    """ Serializer for user trackings. """

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        """
        Check that start_tracking_date is before end_tracking_date.
        """

        if data['start_tracking_date'] > data['end_tracking_date']:
            raise serializers.ValidationError("end must occur after start")

        if data['end_tracking_date'] - data['start_tracking_date'] < \
           timedelta(hours=data["tracking_interval"]):
            raise serializers.ValidationError(
                "Period of tracking is too short for this tracking interval"
            )
        return data

    class Meta:
        model = ProductTracking
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ProductTracking.objects.all(),
                fields=['user', 'product_id']
            )
        ]


class ProductHistorySerializer(serializers.ModelSerializer):
    """ Serializer for product history records. """

    class Meta:
        model = ProductHistory
        fields = '__all__'
