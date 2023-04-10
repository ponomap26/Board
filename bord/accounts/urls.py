from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [

    path('signup/', views.register, name="register"),
    path('codeAp/', views.endreg, name="activation_code"),
]