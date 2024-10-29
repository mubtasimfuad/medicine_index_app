from rest_framework import serializers
from ..models import (
    MedicineDetail,
    GenericName,
    MedicineCategory,
    Manufacturer,
    MedicineForm,
)
from ..exceptions import FeaturedMedicineInvalidError


# Nested serializers for read operations
class GenericNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericName
        fields = ["id", "name"]


class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = ["id", "name"]


class MedicineFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineForm
        fields = ["id", "form_type"]


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ["id", "name"]


# Main serializer for MedicineDetail
class MedicineDetailSerializer(serializers.ModelSerializer):
    # Allow nested detail on read and accept ID on write
    generic_name = serializers.PrimaryKeyRelatedField(
        queryset=GenericName.objects.all(), write_only=True
    )
    generic_name_details = GenericNameSerializer(read_only=True, source="generic_name")

    category = serializers.PrimaryKeyRelatedField(
        queryset=MedicineCategory.objects.all(), write_only=True
    )
    category_details = MedicineCategorySerializer(read_only=True, source="category")

    form = serializers.PrimaryKeyRelatedField(
        queryset=MedicineForm.objects.all(), write_only=True
    )
    form_details = MedicineFormSerializer(read_only=True, source="form")

    manufacturer = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(), allow_null=True, write_only=True
    )
    manufacturer_details = ManufacturerSerializer(read_only=True, source="manufacturer")

    class Meta:
        model = MedicineDetail
        fields = [
            "id",
            "name",
            "description",
            "price",
            "batch_number",
            "stock_quantity",
            "unit_of_measurement",
            "prescription_required",
            "is_available",
            "is_featured",
            "generic_name",
            "generic_name_details",
            "category",
            "category_details",
            "form",
            "form_details",
            "manufacturer",
            "manufacturer_details",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        if data.get("is_featured"):
            existing_featured = MedicineDetail.objects.filter(
                generic_name=data["generic_name"], is_featured=True
            ).exclude(id=self.instance.id if self.instance else None)
            if existing_featured.exists():
                raise FeaturedMedicineInvalidError(
                    "Only one featured medicine is allowed per generic name."
                )
        return data
