from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User


# Placeholder signal handlers (expand later if needed)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Future: create related objects, send welcome email, etc.
        pass
