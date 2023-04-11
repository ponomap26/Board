from django.urls import path


from . import views
from .forms import BlogsDelete
from .views import BlogsList, BlogsDetail, BlogsSearch, BlogsCreate, BlogsUpdate, BlogsDelete

urlpatterns = [
    path('', BlogsList.as_view(), name='blogs'),
    path('<int:pk>', BlogsDetail.as_view(), name='blog'),
    path('search/', BlogsSearch.as_view(), name='search'),
    path('create/', BlogsCreate.as_view(), name='create'),
    path('<int:pk>/delete/', BlogsDelete.as_view(), name='blogs_delete'),
    path('<int:pk>/edit/', BlogsUpdate.as_view(), name='blogs_edit'),
    # path('ads/<int:ad_id>/', views.add_ad, name='add_ad'),
    path('ads/<int:ad_id>/response/', views.add_response, name='add_response'),
    path('ads/<int:ad_id>/response/', views.add_response, name='add_comment_view'),
    # path('categories/<int:pk>', CategoryListView.as_view(), name='category_list')
    # path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
]