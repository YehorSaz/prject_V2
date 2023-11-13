from django.urls import path

from apps.email_to_admin.views import EmailToAdminView

urlpatterns = [
    path('', EmailToAdminView.as_view(), name='email_to_admin')
]