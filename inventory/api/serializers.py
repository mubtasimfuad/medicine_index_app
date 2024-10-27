from rest_framework import serializers
from ..models import (
    MedicineDetail,
    GenericName,
    MedicineCategory,
    Manufacturer,
    MedicineForm,
)
from ..exceptions import FeaturedMedicineInvalidError


class MedicineDetailSerializer(serializers.ModelSerializer):
    generic_name = serializers.PrimaryKeyRelatedField(
        queryset=GenericName.objects.all()
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=MedicineCategory.objects.all()
    )
    form = serializers.PrimaryKeyRelatedField(queryset=MedicineForm.objects.all())
    manufacturer = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(), allow_null=True
    )

    class Meta:
        model = MedicineDetail
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        """Custom validation for ensuring only one featured medicine per generic_name."""
        if data.get("is_featured"):
            # Check if another featured medicine exists for the same generic name
            existing_featured = MedicineDetail.objects.filter(
                generic_name=data["generic_name"], is_featured=True
            ).exclude(id=self.instance.id if self.instance else None)
            if existing_featured.exists():
                raise FeaturedMedicineInvalidError(
                    "Only one featured medicine is allowed per generic name."
                )
        return data
