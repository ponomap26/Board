from django.urls import path


from . import views
from .views import BlogsList, BlogsDetail, BlogsSearch, BlogsCreate, BlogsUpdate, BlogsDelete, add_response, \
    ResponseList, UserResponseListView, ResponseDelete, ResponseSearch,  ResponseDetail

urlpatterns = [
    path('', BlogsList.as_view(), name='blogs'),
    path('<int:pk>', BlogsDetail.as_view(), name='blog'),
    path('search/', BlogsSearch.as_view(), name='search'),
    path('create/', BlogsCreate.as_view(), name='create'),
    path('<int:pk>/delete/', BlogsDelete.as_view(), name='blogs_delete'),
    path('<int:pk>/edit/', BlogsUpdate.as_view(), name='blogs_edit'),

    path('respons_list/', ResponseList.as_view(), name='response_list'),
    path('responses/', UserResponseListView.as_view(), name='user_responses'),
    path('responses/delete/<int:pk>/', ResponseDelete.as_view(), name='responses_delete'),
    path('responses/<int:pk>/', ResponseDetail.as_view(), name='response_detail'),
    path('<int:pk>/response/', add_response, name='add_response'),
    path('responses/search/', ResponseSearch.as_view(), name='response_search'),
    path('responses/accept/<int:response_id>/', views.accept_response, name='accept_response'),
]