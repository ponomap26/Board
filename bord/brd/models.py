from django.db import models
from django.contrib.auth.models import User

"""модель для категорий объявлений"""

# class Category(models.Model):
#     NEWS = "NW"
#     ARTICLE = "AT"
#     CATEGORY_CHOICES = (
#         (NEWS, 'НОВОСТЬ'),
#         (ARTICLE, 'СТАТЬЯ'),)
#     name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)


"""модель для профиля пользователя"""


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', default=None, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True, null=True, default=None)
    date = models.DateField(blank=True, null=True)


""" модель для объявлений"""


class Author(models.Model):
    authorUser = models.ForeignKey(User, on_delete=models.CASCADE, help_text=('Имя Автора'))

    def __str__(self):
        return self.authorUser.username


# class Category(models.Model):
#     NEWS = "NW"
#     ARTICLE = "AT"
#     CATEGORY_CHOICES = (
#         (NEWS, 'НОВОСТЬ'),
#         (ARTICLE, 'СТАТЬЯ'),
#     )
#     name = models.CharField(max_length=200, choices=CATEGORY_CHOICES,
#                             default=ARTICLE, help_text=('Название категории'))
#
#     def __str__(self):
#         return f'{self.name}'


class Ad(models.Model):
    ТАНКИ = "TN"
    ХИЛЫ = "XL"
    ДД = "DD"
    ТОРГОВЦЫ = "TRG"
    ГИЛДМАСТЕРА = 'GIL'
    КВЕСТГИВЕРЫ = 'KVS'

    CATEGORY_CHOICES = (
        (ТАНКИ, 'ТАНКИ'),
        (ХИЛЫ, 'ХИЛЫ'),
        (ДД, 'ДД'),
        (ТОРГОВЦЫ, 'ТОРГОВЦЫ'),
        (ГИЛДМАСТЕРА, 'ГИЛДМАСТЕРА'),
        (КВЕСТГИВЕРЫ, 'КВЕСТГИВЕРЫ'),
    )

    author = models.ForeignKey(Author, on_delete=models.CASCADE, help_text="Автор")
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES,
                                default=ТАНКИ, help_text=('Название категории'))
    # created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True, max_length=255)

    # def __str__(self):
    #     return f'{self.name}'

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

#
# class BlogsCategory(models.Model):
#     blogs = models.ForeignKey(Ad, on_delete=models.CASCADE)
#     category = models.ForeignKey(on_delete=models.CASCADE)

# def __str__(self):
#     return f'{self.name}'
