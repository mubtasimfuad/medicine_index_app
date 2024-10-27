from django.urls import path
from .views import MedicineDetailView

urlpatterns = [
    path("medicines/", MedicineDetailView.as_view(), name="medicine-list"),
    path("medicines/<uuid:pk>/", MedicineDetailView.as_view(), name="medicine-detail"),
]
