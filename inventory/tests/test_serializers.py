# inventory/tests/test_serializers.py

import pytest
from inventory.exceptions import FeaturedMedicineInvalidError
from inventory.models import (
    Manufacturer,
    MedicineCategory,
    MedicineDetail,
    GenericName,
    MedicineForm,
)
from inventory.api.serializers import MedicineDetailSerializer
from decimal import Decimal


@pytest.mark.django_db
def test_medicine_detail_serializer():
    generic_name = GenericName.objects.create(name="Amoxicillin")
    category = MedicineCategory.objects.create(
        name="Antibiotic", description="Antibiotic medication"
    )
    form = MedicineForm.objects.create(form_type="CAPSULE", description="Capsule form")
    manufacturer = Manufacturer.objects.create(
        name="Health Corp", contact_info="987-654-3210"
    )

    data = {
        "name": "Amoxicillin Capsule",
        "generic_name": generic_name.id,
        "category": category.id,
        "form": form.id,
        "manufacturer": manufacturer.id,
        "description": "Antibiotic for infections",
        "price": Decimal("8.99"),
        "batch_number": "B126",
        "is_featured": True,
    }
    serializer = MedicineDetailSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["is_featured"] is True


@pytest.mark.django_db
def test_featured_constraint_in_serializer():
    generic_name = GenericName.objects.create(name="Ciprofloxacin")
    category = MedicineCategory.objects.create(
        name="Antibiotic", description="Antibiotic medication"
    )
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(
        name="Pharma Ltd.", contact_info="789-654-1230"
    )

    # First featured medicine
    MedicineDetail.objects.create(
        name="Ciprofloxacin Tablet",
        generic_name=generic_name,
        category=category,
        form=form,
        manufacturer=manufacturer,
        description="Antibiotic for bacterial infections",
        price=Decimal("9.99"),
        batch_number="B127",
        is_featured=True,
    )

    # Serializer data with duplicate featured constraint
    data = {
        "name": "Ciprofloxacin Syrup",
        "generic_name": generic_name.id,
        "category": category.id,
        "form": form.id,
        "manufacturer": manufacturer.id,
        "description": "Antibiotic in syrup form",
        "price": Decimal("10.99"),
        "batch_number": "B128",
        "is_featured": True,
    }

    serializer = MedicineDetailSerializer(data=data)
    with pytest.raises(
        FeaturedMedicineInvalidError,
        match="Only one featured medicine is allowed per generic name",
    ):
        serializer.is_valid(raise_exception=True)
