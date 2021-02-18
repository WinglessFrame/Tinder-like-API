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


def upload_message_image(instance, filename):
    return f"messages_images/{instance.user}/{filename}"


class Profile(models.Model):
    location = models.PointField(blank=True, null=True)
    subscription = models.CharField(max_length=150, blank=False, null=False, default='default',
                                    choices=SUBSCRIPTION_CHOICES)
    bio = models.TextField(max_length=500, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    viewed = models.ManyToManyField('Profile', related_name='viewed_by', blank=True)
    search_distance = models.IntegerField(blank=True, default=20)

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


# Update search distance when profile subscription is updated
# Gold subscription can be updated through specific endpoint
@receiver(post_save, sender=Profile)
def change_subscription(sender, instance, created, **kwargs):
    if not created:
        if instance.subscription == 'default':
            Profile.objects.filter(pk=instance.pk).update(search_distance=20)
        if instance.subscription == 'silver':
            Profile.objects.filter(pk=instance.pk).update(search_distance=25)


class Post(models.Model):
    image = models.ImageField(upload_to=upload_post_image, blank=False)
    description = models.TextField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='posts')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class MatchChat(models.Model):
    user_profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='matches1', blank=False)
    user_profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='matches2', blank=False)

    def __str__(self):
        return f"{self.user_profile1.user.username}-{self.user_profile2.user.username}"

    class Meta:
        verbose_name = "MatchChat"
        verbose_name_plural = "MatchChats"


class Message(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey(MatchChat, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(max_length=500, blank=False)
    image = models.ImageField(upload_to=upload_message_image, blank=True)

    def __str__(self):
        return f"{self.user.user.username}-{self.chat.pk}"
