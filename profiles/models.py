# profiles/models.py
import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User


def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'avatars/user_{instance.user.id}.{ext}'


def cover_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'covers/user_{instance.user.id}.{ext}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=40, blank=True, default="Ley")
    tagline = models.CharField(max_length=60, blank=True, default="IT")
    bio = models.CharField(max_length=160, blank=True, default="There's a purpose in that pain.")
    thought_bubble = models.CharField(max_length=120, blank=True, default="'yoko na, sainyo nalang lahat 'tooo")

    workplace = models.CharField(max_length=100, blank=True, default="Software Engineer")
    education = models.CharField(max_length=100, blank=True, default="Dalubhasaan ng Lungsod ng Lucena - DLL")
    location = models.CharField(max_length=100, blank=True, default="Lucena")
    lives_in = models.CharField(max_length=100, blank=True, default="Lucena City")
    hometown = models.CharField(max_length=100, blank=True, default="Pagbilao")
    birthday = models.CharField(max_length=60, blank=True, default="August 27")
    social_handle = models.CharField(max_length=60, blank=True, default="yeahmey")

    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    cover_photo = models.ImageField(upload_to=cover_upload_path, blank=True, null=True)
    friends_count = models.PositiveIntegerField(default=497)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        try:
            old_instance = Profile.objects.get(pk=self.pk)
            if old_instance.avatar and old_instance.avatar != self.avatar:
                if os.path.isfile(old_instance.avatar.path):
                    os.remove(old_instance.avatar.path)
            if old_instance.cover_photo and old_instance.cover_photo != self.cover_photo:
                if os.path.isfile(old_instance.cover_photo.path):
                    os.remove(old_instance.cover_photo.path)
        except Profile.DoesNotExist:
            pass

        super().save(*args, **kwargs)

        if self.avatar and os.path.isfile(self.avatar.path):
            img = Image.open(self.avatar.path)
            if img.height > 400 or img.width > 400:
                img.thumbnail((400, 400))
                img.save(self.avatar.path, quality=85, optimize=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def total_likes(self):
        return self.likes.count()