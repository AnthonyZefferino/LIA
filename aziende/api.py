from rest_framework import serializers
from .models import Company, Industry, Sector


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['name']


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['name']


class CompanySerializer(serializers.ModelSerializer):
    industry = IndustrySerializer(read_only=True)
    sector = SectorSerializer(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'  # O specificare i campi necessari
