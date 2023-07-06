from django.urls import path
from .views import DeviceManagementView, DeviceCreateView , DeviceDetailView, DeviceEditView, DeviceDelete

app_name = "device"

urlpatterns = [
  path("management/", DeviceManagementView.as_view(), name="device_management"),
  path("management/<str:pk>/detail/", DeviceDetailView.as_view(), name="device_detail"),
  path("management/create/", DeviceCreateView.as_view(), name="device_create"),
  path("management/<str:pk>/edit/", DeviceEditView.as_view(), name="device_edit"),
  path("management/<str:pk>/delete/", DeviceDelete, name="device_delete"),
]