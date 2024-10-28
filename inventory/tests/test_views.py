from decimal import Decimal
import json
import pytest
import logging
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from inventory.models import (
    MedicineDetail,
    GenericName,
    MedicineCategory,
    MedicineForm,
    Manufacturer,
)
from utils.redis_cache import RedisCache
from django.contrib.auth.models import User

# Set up logging
app_logger = logging.getLogger("app_logger")
error_logger = logging.getLogger("error_logger")

# Initialize the APIClient
client = APIClient()


@pytest.fixture
def admin_user():
    """Create an admin user for authenticated requests."""
    return User.objects.create_superuser(username="admin", password="password123")


@pytest.fixture
def authenticated_client(admin_user):
    """Provide an authenticated client for admin requests."""
    refresh = RefreshToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


# Fixture to clear Redis cache before each test
@pytest.fixture(autouse=True)
def clear_cache():
    cache_manager = RedisCache()
    cache_manager.redis.flushdb()  # Clears all keys in Redis before each test


@pytest.mark.django_db
def test_get_medicine_detail_list(authenticated_client):
    app_logger.info("Testing GET /api/medicines/")

    # First request should populate the cache
    response = authenticated_client.get("/api/medicines/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data["data"], list)

    # Verify cache entry exists after first GET request
    cache_key = "medicine_list"
    cached_data = RedisCache().get(cache_key)
    assert cached_data is not None, "Cache should be populated after first request."


@pytest.mark.django_db
def test_create_medicine_with_featured_constraint(authenticated_client):
    app_logger.info("Testing POST /api/medicines/ with featured constraint")

    # Setting up related objects for medicine
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

    # Create a featured medicine
    response = authenticated_client.post("/api/medicines/", data=data)
    assert response.status_code == status.HTTP_201_CREATED

    # Verify that cache was invalidated after creation
    cache_key = "medicine_list"
    cached_data = RedisCache().get(cache_key)
    assert cached_data is None, "Cache should be cleared after POST request."


@pytest.mark.django_db
def test_update_medicine_detail(authenticated_client):
    app_logger.info("Testing PUT /api/medicines/<pk> for update")

    # Setting up related objects for medicine
    generic_name = GenericName.objects.create(name="Paracetamol")
    category = MedicineCategory.objects.create(
        name="Analgesic", description="Pain reliever"
    )
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(
        name="Pharma Inc.", contact_info="123-456-7890"
    )

    # Creating a medicine entry to update
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

    # Update the medicine
    update_data = {"name": "Paracetamol Extra Strength", "price": Decimal("6.99")}
    response = authenticated_client.put(
        f"/api/medicines/{medicine.pk}/", data=update_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["name"] == "Paracetamol Extra Strength"

    # Verify cache invalidation
    detail_cache_key = f"medicine_detail_{medicine.pk}"
    list_cache_key = "medicine_list"
    assert (
        RedisCache().get(detail_cache_key) is None
    ), "Detail cache should be cleared after update."
    assert (
        RedisCache().get(list_cache_key) is None
    ), "List cache should be cleared after update."


@pytest.mark.django_db
def test_delete_medicine_detail(authenticated_client):
    app_logger.info("Testing DELETE /api/medicines/<pk> for deletion")

    # Setting up related objects for medicine
    generic_name = GenericName.objects.create(name="Amoxicillin")
    category = MedicineCategory.objects.create(
        name="Antibiotic", description="Antibiotic class"
    )
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(
        name="Pharma Co.", contact_info="123-456-7890"
    )

    # Creating a medicine entry to delete
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

    # Deleting the medicine
    response = authenticated_client.delete(f"/api/medicines/{medicine.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Confirm deletion by attempting to retrieve deleted entry
    response = authenticated_client.get(f"/api/medicines/{medicine.pk}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Verify cache invalidation after deletion
    detail_cache_key = f"medicine_detail_{medicine.pk}"
    list_cache_key = "medicine_list"
    assert (
        RedisCache().get(detail_cache_key) is None
    ), "Detail cache should be cleared after deletion."
    assert (
        RedisCache().get(list_cache_key) is None
    ), "List cache should be cleared after deletion."

@pytest.mark.django_db
def test_medicine_search(authenticated_client):
    app_logger.info("Testing GET /api/medicines/search/ with various queries and filters")

    # Set up sample medicines with varying names and categories
    generic_name1 = GenericName.objects.create(name="Ibuprofen")
    generic_name2 = GenericName.objects.create(name="Amoxicillin")
    category1 = MedicineCategory.objects.create(name="Painkiller", description="Pain relief")
    category2 = MedicineCategory.objects.create(name="Antibiotic", description="Antibiotic class")
    form = MedicineForm.objects.create(form_type="TABLET", description="Tablet form")
    manufacturer = Manufacturer.objects.create(name="HealthCorp", contact_info="123-456-7890")

    # Create medicines with varied names, generic names, and categories
    MedicineDetail.objects.create(
        name="Ibuprofen Tablet",
        generic_name=generic_name1,
        category=category1,
        form=form,
        manufacturer=manufacturer,
        description="Relieves pain",
        price=Decimal("9.99"),
        batch_number="B100",
        is_featured=False,
    )
    MedicineDetail.objects.create(
        name="Amoxicillin Capsule",
        generic_name=generic_name2,
        category=category2,
        form=form,
        manufacturer=manufacturer,
        description="Used to treat bacterial infections",
        price=Decimal("15.99"),
        batch_number="B101",
        is_featured=True,
    )

    # Perform a search for "Ibuprofen" and verify correct results
    search_query = {"q": "Ibuprofen"}
    response = authenticated_client.get("/api/medicines/search/", search_query)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["data"]) == 1
    assert response.data["data"][0]["name"] == "Ibuprofen Tablet"

    # Verify search result caching by checking if Redis cache exists
    cache_key = f"medicine_search_{search_query['q']}"
    cached_data = RedisCache().get(cache_key)
    assert cached_data is not None, "Search results should be cached after initial query."

    # Perform a search with filters applied (e.g., category = "Antibiotic")
    search_query_with_filter = {"q": "Amoxicillin", "filters": json.dumps({"category": category2.id})}
    response = authenticated_client.get("/api/medicines/search/", search_query_with_filter)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["data"]) == 1
    assert response.data["data"][0]["name"] == "Amoxicillin Capsule"

    # Verify cache invalidation works by updating a medicine and ensuring cache is cleared
    medicine = MedicineDetail.objects.get(name="Ibuprofen Tablet")
    medicine.price = Decimal("11.99")
    medicine.save()

    # Check cache for the "Ibuprofen" query after the update to ensure invalidation
    assert RedisCache().get(cache_key) is None, "Cache should be invalidated after updating medicine data."

    # Retry search after invalidation to ensure fresh data
    response = authenticated_client.get("/api/medicines/search/", search_query)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["data"]) == 1
    assert response.data["data"][0]["price"] == "11.99", "Updated price should reflect in search results"
