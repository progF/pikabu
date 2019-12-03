from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import MainUser, Profile
from utils.file_upload import media_delete_path
from django.core.mail import send_mail


@receiver(post_save, sender=MainUser, dispatch_uid="_uid")
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if instance.email:
            send_mail(
                'Спасибо, что зарегались!',
                'Мы любим вас! Особенно за то, что указали почту.',
                'pikabu.team@example.com',
                [instance.email],
                fail_silently=False,
            )


@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    if instance.profile_image or instance.background_image:
        try:
            media_delete_path(instance.profile_image)
        except Exception:
            media_delete_path(instance.background_image)
