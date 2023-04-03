from django.urls import path

from bord.brd.views import BlogsList, BlogsDetail, BlogsSearch

urlpatterns = [
    path('', BlogsList.as_view(), name='blogs'),
    path('<int:pk>', BlogsDetail.as_view(), name='blog'),
    path('search/', BlogsSearch.as_view(), name='search'),
    # path('create/', PostCreate.as_view(), name='news_create'),
    # path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
]