from django.contrib import admin

# Register your models here.
from brd.models import Ad, Author, Response, Profile, Notification

admin.site.register(Ad)
admin.site.register(Author)
admin.site.register(Response)
admin.site.register(Profile)
admin.site.register(Notification)