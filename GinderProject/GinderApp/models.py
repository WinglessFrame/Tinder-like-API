from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

SUBSCRIPTION_CHOICES = (
    ('default', 'Default'),
    ('silver', 'Silver'),
    ('gold', 'Gold'),
)


def upload_post_image(instance, filename):
    return f"posts/{instance.user}/{filename}"


class Profile(models.Model):
    location = models.PointField(blank=True, null=True)
    subscription = models.CharField(max_length=150, blank=False, null=False, default='default',
                                    choices=SUBSCRIPTION_CHOICES)
    bio = models.TextField(max_length=500, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    image = models.ImageField(upload_to=upload_post_image, blank=False)
    description = models.TextField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
