# api/models.py
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.core.files.storage import default_storage
from django_resized import ResizedImageField

User = get_user_model()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Album(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Picture(models.Model):
    album = models.ForeignKey(Album, related_name='pictures', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='pictures', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    size = models.IntegerField(null=True)
    type = models.CharField(max_length=100, blank=True)
    url = models.ImageField(upload_to='pictures', blank=True)
    thumbnailUrl = ResizedImageField(size=[100, 100], crop=['middle', 'center'], upload_to='thumbnails', blank=True)

    def __str__(self):
        return self.url