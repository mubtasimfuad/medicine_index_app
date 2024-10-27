import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

# Enum choices for unit of measurement
class UnitOfMeasurement(models.TextChoices):
    TABLET = "TBL", _("Tablet")
    CAPSULE = "CAP", _("Capsule")
    SYRUP = "SYR", _("Syrup")
    OINTMENT = "ONT", _("Ointment")
    OTHER = "OTH", _("Other")


# Enum choices for MedicineCategory type
class CategoryType(models.TextChoices):
    ANTIBIOTIC = "ANT", _("Antibiotic")
    ANALGESIC = "ANL", _("Analgesic")
    ANTIPYRETIC = "APR", _("Antipyretic")
    VITAMIN = "VIT", _("Vitamin")
    SUPPLEMENT = "SUP", _("Supplement")
    OTHER = "OTH", _("Other")


class MedicineCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    category_type = models.CharField(
        max_length=3, choices=CategoryType.choices, default=CategoryType.OTHER
    )
    image = models.ImageField(
        upload_to="category_images/", blank=True, default="default_image.jpg"
    )

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"


# Enum choices for MedicineForm type
class FormType(models.TextChoices):
    TABLET = "TBL", _("Tablet")
    SYRUP = "SYR", _("Syrup")
    INJECTION = "INJ", _("Injection")
    OINTMENT = "ONT", _("Ointment")
    DROPS = "DRP", _("Drops")
    OTHER = "OTH", _("Other")


class MedicineForm(models.Model):
    form_type = models.CharField(max_length=100, choices=FormType.choices, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.get_form_type_display()


class GenericName(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TherapeuticClass(models.Model):
    name = models.CharField(max_length=100)
    subclass_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ["name", "subclass_name"]

    def __str__(self):
        return f"{self.name} - {self.subclass_name}"


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    contact_info = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(
        upload_to="manufacturer_images/", blank=True, default="default_logo.jpg"
    )

    def __str__(self):
        return self.name


from django.core.exceptions import ValidationError


class MedicineDetail(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    generic_name = models.ForeignKey(
        GenericName, on_delete=models.PROTECT, related_name="medicines"
    )
    category = models.ForeignKey(
        MedicineCategory, on_delete=models.PROTECT, related_name="medicines"
    )
    form = models.ForeignKey(
        MedicineForm, on_delete=models.PROTECT, related_name="medicines"
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, related_name="medicines"
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    batch_number = models.CharField(max_length=100, unique=True, db_index=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    unit_of_measurement = models.CharField(
        max_length=3,
        choices=UnitOfMeasurement.choices,
        default=UnitOfMeasurement.TABLET,
    )
    prescription_required = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)  # New field for featured medicines
    conditions = models.ManyToManyField(
        Condition, blank=True, related_name="medications"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Check if another featured medicine exists with the same generic name
        if self.is_featured:
            existing_featured = MedicineDetail.objects.filter(
                generic_name=self.generic_name, is_featured=True
            ).exclude(
                id=self.id
            )  # Exclude self in case of update
            if existing_featured.exists():
                raise ValidationError(
                    f"There can only be one featured medicine for the generic name '{self.generic_name}'."
                )

    def save(self, *args, **kwargs):
        # Call the full_clean method before saving to ensure clean() is run
        self.full_clean()  # This triggers the clean() method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.generic_name.name})"

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("name", "batch_number")


class PracticeUpdate(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(
        max_length=100, blank=True, null=True
    )  # Optional category
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
