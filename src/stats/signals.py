import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .models import ProductTracking


@receiver(post_save, sender=ProductTracking)
def create_or_update_periodic_task(sender, instance, created, **kwargs):
    if created:
        interval, created = IntervalSchedule.objects.get_or_create(
            every=instance.tracking_interval,
            period=IntervalSchedule.HOURS,
        )
        PeriodicTask.objects.create(
            name=f"parse_product_{instance.product_id}_for_user_{instance.user}",
            task="parse_and_save_product_history",
            interval=interval,
            enabled=True,
            start_time=instance.start_tracking_date,
            expires=instance.end_tracking_date,
            kwargs=json.dumps(
                {
                    "product_id": instance.product_id,
                    "tracking_id": instance.id,
                }
            )
        )

    # need to add code for updating celery tasks
