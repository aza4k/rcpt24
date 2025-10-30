from rest_framework import serializers
from .models import Medicine, Pharmacy, Inventory

class MedicineSearchSerializer(serializers.ModelSerializer):
    price_min = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    pharmacies_count = serializers.IntegerField(required=False)

    class Meta:
        model = Medicine
        fields = ["id", "name", "slug", "price_min", "pharmacies_count"]

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ["id", "name", "address", "phone", "lat", "lng", "working_hours"]

class InventorySerializer(serializers.ModelSerializer):
    pharmacy = PharmacySerializer()
    class Meta:
        model = Inventory
        fields = ["id", "pharmacy", "quantity", "price"]
