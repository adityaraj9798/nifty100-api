from rest_framework import serializers
from .models import DimCompany, FactProfitLoss, FactBalanceSheet

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = DimCompany
        fields = ['symbol', 'logo_url', 'company_name', 'chart_link', 'description', 'website']

class ProfitLossSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactProfitLoss
        fields = '__all__'

class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactBalanceSheet
        fields = '__all__'