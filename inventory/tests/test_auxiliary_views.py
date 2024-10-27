import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


client = APIClient()

@pytest.fixture
def admin_user():
    user = User.objects.create_superuser(username="admin", password="adminpass")
    client.login(username="admin", password="adminpass")
    return user

@pytest.fixture
def regular_user():
    user = User.objects.create_user(username="user", password="userpass")
    client.login(username="user", password="userpass")
    return user


@pytest.mark.django_db
def test_generic_name_crud(admin_user):
    """CRUD operations for GenericName model"""
    client.force_authenticate(user=admin_user)

    # Create
    generic_data = {"name": "Test Generic"}
    response = client.post("/api/generic-names/", data=generic_data)
    print("CREATE GenericName Response:", response.status_code, response.data) 
    assert response.status_code == status.HTTP_201_CREATED, f"Failed to create: {response.data}"
    generic_id = response.data["data"]["id"]

    # Retrieve
    response = client.get(f"/api/generic-names/{generic_id}/")
    print("RETRIEVE GenericName Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_200_OK, f"Failed to retrieve: {response.data}"
    assert response.data["data"]["name"] == "Test Generic"

    # Update
    response = client.put(f"/api/generic-names/{generic_id}/", data={"name": "Updated Generic"})
    print("UPDATE GenericName Response:", response.status_code, response.data) 
    assert response.status_code == status.HTTP_200_OK, f"Failed to update: {response.data}"
    assert response.data["data"]["name"] == "Updated Generic"

    # Delete
    response = client.delete(f"/api/generic-names/{generic_id}/")
    print("DELETE GenericName Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_204_NO_CONTENT, f"Failed to delete: {response.data}"


@pytest.mark.django_db
def test_medicine_category_crud(admin_user):
    """CRUD operations for MedicineCategory model"""
    client.force_authenticate(user=admin_user)

    # Create
    category_data = {"name": "Test Category", "description": "Category Description"}
    response = client.post("/api/categories/", data=category_data)
    print("CREATE MedicineCategory Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_201_CREATED, f"Failed to create: {response.data}"
    category_id = response.data["data"]["id"]

    # Retrieve
    response = client.get(f"/api/categories/{category_id}/")
    print("RETRIEVE MedicineCategory Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_200_OK, f"Failed to retrieve: {response.data}"
    assert response.data["data"]["name"] == "Test Category"

    # Update
    response = client.put(f"/api/categories/{category_id}/", data={"name": "Updated Category"})
    print("UPDATE MedicineCategory Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_200_OK, f"Failed to update: {response.data}"
    assert response.data["data"]["name"] == "Updated Category"

    # Delete
    response = client.delete(f"/api/categories/{category_id}/")
    print("DELETE MedicineCategory Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_204_NO_CONTENT, f"Failed to delete: {response.data}"


@pytest.mark.django_db
def test_medicine_form_crud(admin_user):
    """CRUD operations for MedicineForm model"""
    client.force_authenticate(user=admin_user)

    # Create
    form_data = {"form_type": "SYR", "description": "Syrup form"}
    response = client.post("/api/forms/", data=form_data)
    print("CREATE MedicineForm Response:", response.status_code, response.data)  # Debug
    assert response.status_code == status.HTTP_201_CREATED, f"Failed to create: {response.data}"
    form_id = response.data["data"]["id"]

    # Retrieve
    response = client.get(f"/api/forms/{form_id}/")
    print("RETRIEVE MedicineForm Response:", response.status_code, response.data) 
    assert response.status_code == status.HTTP_200_OK, f"Failed to retrieve: {response.data}"
    assert response.data["data"]["form_type"] == "SYR"

    # Update
    response = client.put(f"/api/forms/{form_id}/", data={"description": "Updated Syrup form"})
    print("UPDATE MedicineForm Response:", response.status_code, response.data) 
    assert response.status_code == status.HTTP_200_OK, f"Failed to update: {response.data}"
    assert response.data["data"]["description"] == "Updated Syrup form"

    # Delete
    response = client.delete(f"/api/forms/{form_id}/")
    print("DELETE MedicineForm Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_204_NO_CONTENT, f"Failed to delete: {response.data}"


@pytest.mark.django_db
def test_manufacturer_crud(admin_user):
    """CRUD operations for Manufacturer model"""
    client.force_authenticate(user=admin_user)

    # Create
    manufacturer_data = {"name": "Test Manufacturer", "contact_info": "123-456-7890"}
    response = client.post("/api/manufacturers/", data=manufacturer_data)
    print("CREATE Manufacturer Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_201_CREATED, f"Failed to create: {response.data}"
    manufacturer_id = response.data["data"]["id"]

    # Retrieve
    response = client.get(f"/api/manufacturers/{manufacturer_id}/")
    print("RETRIEVE Manufacturer Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_200_OK, f"Failed to retrieve: {response.data}"
    assert response.data["data"]["name"] == "Test Manufacturer"

    # Update
    response = client.put(f"/api/manufacturers/{manufacturer_id}/", data={"contact_info": "098-765-4321"})
    print("UPDATE Manufacturer Response:", response.status_code, response.data)
    assert response.status_code == status.HTTP_200_OK, f"Failed to update: {response.data}"
    assert response.data["data"]["contact_info"] == "098-765-4321"

    # Delete
    response = client.delete(f"/api/manufacturers/{manufacturer_id}/")
    print("DELETE Manufacturer Response:", response.status_code, response.data)  
    assert response.status_code == status.HTTP_204_NO_CONTENT, f"Failed to delete: {response.data}"

    client.logout()
