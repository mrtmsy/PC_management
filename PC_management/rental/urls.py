from django.contrib import admin
from django.urls import path
from .views import RentalManagementView, RentalDetailView, RentalCreateview, RentalEditView, RentalDelete

app_name = "rental"

urlpatterns = [
  path("management/",RentalManagementView.as_view(), name="rental_management"),
  path("management/<int:pk>/detail/",RentalDetailView.as_view(), name="rental_detail"),
  path("management/create/", RentalCreateview.as_view(), name="rental_create"),
  path("management/<int:pk>/edit/", RentalEditView.as_view(), name="rental_edit"),
  path('management/<int:pk>/delete/', RentalDelete, name='rental_delete'),
]
