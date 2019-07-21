from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


class Profile(models.Model):

    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='media-storage/images/profile-pic', blank=True, null=True)
    background_pic = models.ImageField(
        upload_to='media-storage/images/background-pic', blank=True, null=True)
    short_bio = models.CharField(max_length=500, blank=True, null=True)
    portfolio = models.URLField(
        verbose_name='Portfolio', blank=True, null=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs["created"]:
        p = Profile(user=kwargs["instance"],)
        p.save()


post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
