from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .tasks import notify_subscribers

@receiver(post_save, sender=News)
def article_created(sender, instance, created, **kwargs):
    if created:
        notify_subscribers(instance)