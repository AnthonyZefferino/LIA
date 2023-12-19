from rest_framework import serializers
from aziende.models import Company
from .models import Project





class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']


class ProjectSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    lead_partner = CompanySerializer(many=True, read_only=True)
    partner = CompanySerializer(many=True, read_only=True)
    supporters = CompanySerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id','company','lead_partner','partner','supporters','project_title','status','description','start_date','end_date']
