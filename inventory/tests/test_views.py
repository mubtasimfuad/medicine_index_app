from decimal import Decimal
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from inventory.models import (
    MedicineDetail,
    GenericName,
    MedicineCategory,
    MedicineForm,
    Manufacturer,
)

client = APIClient()


@pytest.mark.django_db
def test_get_medicine_detail_list():
    # Ensure the endpoint is accessible
    response = client.get("/api/medicines/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data["data"], list)


@pytest.mark.django_db
def test_create_medicine_with_featured_constraint():
    generic_name = GenericName.objects.create(name="Azithromycin")
    category = MedicineCategory.objects.create(
        name="Antibiotic", description="Antibiotic class"
    )
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(
        name="Pharma Co.", contact_info="123-456-7890"
    )

    data = {
        "name": "Azithromycin Tablet",
        "generic_name": generic_name.id,
        "category": category.id,
        "form": form.id,
        "manufacturer": manufacturer.id,
        "description": "Antibiotic tablet for bacterial infections",
        "price": Decimal("15.99"),
        "batch_number": "B129",
        "is_featured": True,
    }

    # First request to create a featured medicine
    response = client.post("/api/medicines/", data=data)
    assert response.status_code == status.HTTP_201_CREATED

    # Attempt to create another featured medicine for the same generic name
    data["name"] = "Azithromycin Syrup"
    data["batch_number"] = "B130"  # Ensure unique batch number
    response = client.post("/api/medicines/", data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Adjust assertion to check within the custom response structure
    assert (
        "Only one featured medicine is allowed per generic name"
        in response.data["message"]
    )


@pytest.mark.django_db
def test_update_medicine_detail():
    # Setup initial data
    generic_name = GenericName.objects.create(name="Paracetamol")
    category = MedicineCategory.objects.create(
        name="Analgesic", description="Pain reliever"
    )
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(
        name="Pharma Inc.", contact_info="123-456-7890"
    )

    # Create a medicine entry
    medicine = MedicineDetail.objects.create(
        name="Paracetamol Tablet",
        generic_name=generic_name,
        category=category,
        form=form,
        manufacturer=manufacturer,
        description="Pain relief",
        price=Decimal("5.99"),
        batch_number="B123",
        is_featured=True,
    )

    # Update the medicine entry
    update_data = {"name": "Paracetamol Extra Strength", "price": Decimal("6.99")}
    response = client.put(
        f"/api/medicines/{medicine.pk}/", data=update_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["name"] == "Paracetamol Extra Strength"
    assert response.data["data"]["price"] == "6.99"


@pytest.mark.django_db
def test_partial_update_medicine_detail():
    # Setup initial data
    generic_name = GenericName.objects.create(name="Ibuprofen")
    category = MedicineCategory.objects.create(
        name="Analgesic", description="Pain reliever"
    )
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(
        name="Pharma Inc.", contact_info="123-456-7890"
    )

    # Create a medicine entry
    medicine = MedicineDetail.objects.create(
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

    # Perform a partial update (e.g., only update the description)
    partial_update_data = {"description": "Updated pain relief description"}
    response = client.put(
        f"/api/medicines/{medicine.pk}/",
        data=partial_update_data,
        format="json",
        partial=True,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["description"] == "Updated pain relief description"


@pytest.mark.django_db
def test_delete_medicine_detail():
    # Setup initial data
    generic_name = GenericName.objects.create(name="Amoxicillin")
    category = MedicineCategory.objects.create(
        name="Antibiotic", description="Antibiotic class"
    )
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(
        name="Pharma Co.", contact_info="123-456-7890"
    )

    # Create a medicine entry
    medicine = MedicineDetail.objects.create(
        name="Amoxicillin Tablet",
        generic_name=generic_name,
        category=category,
        form=form,
        manufacturer=manufacturer,
        description="Antibiotic medication",
        price=Decimal("15.99"),
        batch_number="B125",
    )

    # Delete the medicine entry
    response = client.delete(f"/api/medicines/{medicine.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Confirm the entry no longer exists
    response = client.get(f"/api/medicines/{medicine.pk}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
