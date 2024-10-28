# inventory/api/urls.py
from django.urls import path
from .views import MedicineDetailView, MedicineListView
from .auxiliary_views import (
    GenericNameListCreateView,
    GenericNameRetrieveUpdateDestroyView,
    MedicineCategoryListCreateView,
    MedicineCategoryRetrieveUpdateDestroyView,
    MedicineFormListCreateView,
    MedicineFormRetrieveUpdateDestroyView,
    ManufacturerListCreateView,
    ManufacturerRetrieveUpdateDestroyView,
)

urlpatterns = [
     path("medicines/", MedicineListView.as_view(), name="medicine-list"),
    path("medicines/<uuid:pk>/", MedicineDetailView.as_view(), name="medicine-detail"),

    path(
        "generic-names/", GenericNameListCreateView.as_view(), name="generic-name-list"
    ),
    path(
        "generic-names/<int:pk>/",
        GenericNameRetrieveUpdateDestroyView.as_view(),
        name="generic-name-detail",
    ),
    path("categories/", MedicineCategoryListCreateView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>/",
        MedicineCategoryRetrieveUpdateDestroyView.as_view(),
        name="category-detail",
    ),
    path("forms/", MedicineFormListCreateView.as_view(), name="form-list"),
    path(
        "forms/<int:pk>/",
        MedicineFormRetrieveUpdateDestroyView.as_view(),
        name="form-detail",
    ),
    path(
        "manufacturers/", ManufacturerListCreateView.as_view(), name="manufacturer-list"
    ),
    path(
        "manufacturers/<int:pk>/",
        ManufacturerRetrieveUpdateDestroyView.as_view(),
        name="manufacturer-detail",
    ),
]
