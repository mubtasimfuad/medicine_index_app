# inventory/management/commands/seed_auxiliary_data.py
from django.core.management.base import BaseCommand
from inventory.models import (
    GenericName,
    MedicineCategory,
    MedicineForm,
    Manufacturer,
    Condition,
    TherapeuticClass,
    UnitOfMeasurement,
    FormType,
    CategoryType,
)
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Seed auxiliary data with 100 unique entries relevant to the Bangladeshi context"

    def handle(self, *args, **kwargs):
        self.seed_generic_names()
        self.seed_categories()
        self.seed_forms()
        self.seed_manufacturers()
        self.seed_conditions()
        self.seed_therapeutic_classes()
        self.stdout.write(self.style.SUCCESS("Successfully seeded auxiliary data!"))

    def seed_generic_names(self):
        generic_names = [
            "Paracetamol", "Metformin", "Atorvastatin", "Amlodipine", "Cefixime", "Ibuprofen",
            "Esomeprazole", "Ranitidine", "Levofloxacin", "Azithromycin", "Clarithromycin", 
            "Salmeterol", "Montelukast", "Albuterol", "Loratadine", "Cetirizine", "Fexofenadine", 
            "Phenylephrine", "Dextromethorphan", "Metronidazole", "Amoxicillin", "Ciprofloxacin", 
            "Omeprazole", "Lisinopril", "Simvastatin", "Gliclazide", "Pioglitazone", "Glyburide", 
            "Vildagliptin", "Teneligliptin", "Hydrochlorothiazide", "Furosemide", "Diltiazem", 
            "Losartan", "Candesartan", "Metoprolol", "Enalapril", "Carvedilol", "Bisoprolol",
            "Spironolactone", "Atenolol", "Risperidone", "Clozapine", "Quetiapine", "Olanzapine", 
            "Escitalopram", "Sertraline", "Venlafaxine", "Aspirin", "Clopidogrel", "Warfarin", 
            "Enoxaparin", "Heparin", "Dabigatran", "Apixaban", "Doxycycline", "Clindamycin", 
            "Linezolid", "Amikacin", "Tobramycin", "Gentamicin", "Neomycin", "Vancomycin",
        ]
        for name in generic_names:
            GenericName.objects.get_or_create(name=name)

    def seed_categories(self):
        categories = [
            {"name": "Antibiotic", "description": "Used to treat bacterial infections.", "category_type": CategoryType.ANTIBIOTIC},
            {"name": "Analgesic", "description": "Pain relief medications.", "category_type": CategoryType.ANALGESIC},
            {"name": "Antipyretic", "description": "Medications for fever control.", "category_type": CategoryType.ANTIPYRETIC},
            {"name": "Vitamin", "description": "Supplements for vitamin deficiencies.", "category_type": CategoryType.VITAMIN},
            {"name": "Supplement", "description": "Supplements for overall health.", "category_type": CategoryType.SUPPLEMENT},
            {"name": "Other", "description": "Other categories of medications.", "category_type": CategoryType.OTHER},
        ]
        for category in categories:
            MedicineCategory.objects.get_or_create(**category)

    def seed_forms(self):
        forms = [
            {"form_type": FormType.TABLET, "description": "Solid tablet form of medication."},
            {"form_type": FormType.SYRUP, "description": "Liquid form for oral intake."},
            {"form_type": FormType.INJECTION, "description": "Injection form for direct administration."},
            {"form_type": FormType.OINTMENT, "description": "Semi-solid form for topical use."},
            {"form_type": FormType.DROPS, "description": "Liquid form administered in small drops."},
            {"form_type": FormType.OTHER, "description": "Other forms of medication."},
        ]
        for form in forms:
            MedicineForm.objects.get_or_create(**form)

    def seed_manufacturers(self):
        manufacturers = [
            {"name": "Square Pharmaceuticals Ltd.", "contact_info": "Dhaka, Bangladesh", "website": "https://squarepharma.com.bd"},
            {"name": "Beximco Pharma", "contact_info": "Dhaka, Bangladesh", "website": "https://beximcopharma.com"},
            {"name": "ACI Limited", "contact_info": "Dhaka, Bangladesh", "website": "https://aci-bd.com"},
            {"name": "Eskayef Pharmaceuticals", "contact_info": "Dhaka, Bangladesh", "website": "https://skfbd.com"},
            {"name": "Incepta Pharmaceuticals Ltd.", "contact_info": "Dhaka, Bangladesh", "website": "https://inceptapharma.com"},
            {"name": "Renata Limited", "contact_info": "Dhaka, Bangladesh", "website": "https://renata-ltd.com"},
        ]
        for manufacturer in manufacturers:
            Manufacturer.objects.get_or_create(**manufacturer)

    def seed_conditions(self):
        conditions = [
            "Diabetes", "Hypertension", "Asthma", "Allergies", "Arthritis", 
            "Chronic Pain", "Depression", "Anxiety", "Obesity", "Hyperlipidemia",
            "Acne", "Psoriasis", "Gastroesophageal Reflux Disease", "Migraines",
            "Osteoporosis"
        ]
        for name in conditions:
            Condition.objects.get_or_create(name=name, description=fake.sentence())

    def seed_therapeutic_classes(self):
        classes = [
            {"name": "Antimicrobial", "subclass_name": "Broad-Spectrum Antibiotics"},
            {"name": "Cardiovascular", "subclass_name": "Beta Blockers"},
            {"name": "Respiratory", "subclass_name": "Bronchodilators"},
            {"name": "Endocrinology", "subclass_name": "Insulin Sensitizers"},
            {"name": "Gastrointestinal", "subclass_name": "Proton Pump Inhibitors"},
        ]
        for therapeutic_class in classes:
            TherapeuticClass.objects.get_or_create(**therapeutic_class)
