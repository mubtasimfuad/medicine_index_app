from django.contrib import admin
from .models import (
    MedicineCategory,
    GenericName,
    MedicineForm,
    Manufacturer,
    Condition,
    MedicineDetail,
    TherapeuticClass,
    PracticeUpdate,
)

admin.site.register(MedicineCategory)
admin.site.register(GenericName)
admin.site.register(MedicineForm)
admin.site.register(Manufacturer)
admin.site.register(Condition)


class MedicineDetailAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "generic_name",
        "manufacturer",
        "is_featured",
        "is_available",
    ]
    list_filter = ["is_featured", "manufacturer", "generic_name"]
    search_fields = ["name", "generic_name__name", "manufacturer__name"]


admin.site.register(MedicineDetail, MedicineDetailAdmin)
admin.site.register(TherapeuticClass)
admin.site.register(PracticeUpdate)
