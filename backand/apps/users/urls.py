from django.urls import path

from .views import (
    AdminToUserView,
    BlockUserView,
    DeleteUserView,
    SetAccountStatusBaseView,
    SetAccountStatusPremiumView,
    UnBlockUserView,
    UserListCreateView,
    UserToAdminView,
)

urlpatterns = [
    path('', UserListCreateView.as_view(), name='users_create'),
    path('/<int:pk>/to_admin', UserToAdminView.as_view(), name='user_to_admin'),
    path('/<int:pk>/to_user', AdminToUserView.as_view(), name='admin_to_user'),
    path('/<int:pk>/block', BlockUserView.as_view(), name='block_user'),
    path('/<int:pk>/unblock', UnBlockUserView.as_view(), name='unblock_user'),
    path('/<int:pk>/premium', SetAccountStatusPremiumView.as_view(), name='set_premium'),
    path('/<int:pk>/base', SetAccountStatusBaseView.as_view(), name='set_base'),
    path('/<int:pk>/delete', DeleteUserView.as_view(), name='del_user')
]
