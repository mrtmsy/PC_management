from django.contrib import admin
from django.urls import path
from .views import UserManagementView, UsersDetailView, UsersCreateView, UsersEditView, UsersRetirement, UsersDelete

app_name = "users"

urlpatterns = [
  path("management/", UserManagementView.as_view(), name="users_management"),
  path("management/<str:pk>/detail/", UsersDetailView.as_view(), name="users_detail"),
  path("management/create/", UsersCreateView.as_view(), name="users_create"),
  path("management/<str:pk>/edit/", UsersEditView.as_view(), name="users_edit"),
  path('management/<str:pk>/retirement/', UsersRetirement, name='users_retirement'),
  path('management/<str:pk>/delete/', UsersDelete, name='users_delete'),
]
