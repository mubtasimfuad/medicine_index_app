import pytest
from inventory.exceptions import FeaturedMedicineInvalidError, ValidationError
from inventory.models import (
    Manufacturer,
    MedicineCategory,
    MedicineDetail,
    GenericName,
    MedicineForm,
)


from decimal import Decimal
import logging

logging.basicConfig(level=logging.INFO)


@pytest.mark.django_db
def test_create_medicine_detail():
    generic_name = GenericName.objects.create(name="Paracetamol")
    category = MedicineCategory.objects.create(
        name="Analgesic", description="Pain reliever"
    )
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(
        name="Pharma Inc.", contact_info="123-456-7890"
    )

    # Create medicine with all required fields, explicitly using Decimal for price
    medicine = MedicineDetail.objects.create(
        name="Paracetamol Tablet",
        generic_name=generic_name,
        category=category,
        form=form,
        manufacturer=manufacturer,
        description="Pain relief medication",
        price=Decimal("5.99"),
        batch_number="B123",
        is_featured=True,
    )
    assert medicine.is_featured is True


import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from inventory.models import (
    Manufacturer,
    MedicineCategory,
    MedicineDetail,
    GenericName,
    MedicineForm,
)


@pytest.mark.django_db
def test_featured_medicine_constraint():
    generic_name = GenericName.objects.create(name="Ibuprofen")
    category = MedicineCategory.objects.create(
        name="Analgesic", description="Pain reliever"
    )
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(
        name="Pharma Inc.", contact_info="123-456-7890"
    )

    # Create the first featured medicine
    MedicineDetail.objects.create(
        name="Ibuprofen Tablet",
        generic_name=generic_name,
        category=category,
        form=form,
        manufacturer=manufacturer,
        description="Pain relief medication",
        price=Decimal("10.99"),
        batch_number="B124",
        is_featured=True,
    )

    # Attempt to add another featured medicine for the same generic name
    with pytest.raises(ValidationError) as exc_info:
        MedicineDetail.objects.create(
            name="Ibuprofen Syrup",
            generic_name=generic_name,
            category=category,
            form=form,
            manufacturer=manufacturer,
            description="Pain relief medication",
            price=Decimal("12.99"),
            batch_number="B125",
            is_featured=True,
        )

    assert "__all__" in exc_info.value.message_dict
    assert (
        "There can only be one featured medicine for the generic name"
        in exc_info.value.message_dict["__all__"][0]
    )
