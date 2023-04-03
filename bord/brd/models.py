from django.db import models
from django.contrib.auth.models import User

"""модель для категорий объявлений"""


class Category(models.Model):
    name = models.CharField(max_length=50)


"""модель для профиля пользователя"""


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


""" модель для объявлений"""


class Ad(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


"""модель для откликов"""


class Response(models.Model):
    content = models.TextField()
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


"""модель для уведомлений"""


class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
