from django.urls import path

from apps.posts.views import (
    PostRetriveUpdateDestroyView,
    SetPostActiveView,
    SetPostInActiveView,
    UserAddPostView,
    UserPostListView,
)

urlpatterns =[
    path('', UserPostListView.as_view(), name='user_post_list'),
    path('/create', UserAddPostView.as_view(), name='user_post_create'),
    path('/<int:pk>', PostRetriveUpdateDestroyView.as_view(), name='get_post_by_id'),
    path('/<int:pk>/active', SetPostActiveView.as_view(), name='set_post_status_active'),
    path('/<int:pk>/inactive', SetPostInActiveView.as_view(), name='set_post_status_inactive')
]