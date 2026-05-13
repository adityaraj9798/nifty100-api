from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DimCompany, FactProfitLoss, FactBalanceSheet
from .serializers import CompanySerializer, ProfitLossSerializer, BalanceSheetSerializer

@api_view(['GET'])
def get_companies(request):
    # Exclude the 'id' header row we saw in image_df2311.png
    companies = DimCompany.objects.exclude(symbol='id')
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_company_detail(request, symbol):
    try:
        company = DimCompany.objects.get(symbol=symbol)
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    except DimCompany.DoesNotExist:
        return Response({"error": "Company not found"}, status=404)

@api_view(['GET'])
def get_company_intelligence(request, symbol):
    try:
        # 1. Get Company Profile
        company = DimCompany.objects.get(symbol=symbol)
        
        # 2. Get Financial History (Fact Tables)
        pl_data = FactProfitLoss.objects.filter(symbol=symbol).order_by('-year')
        bs_data = FactBalanceSheet.objects.filter(symbol=symbol).order_by('-year')
        
        return Response({
            "profile": CompanySerializer(company).data,
            "profit_loss": ProfitLossSerializer(pl_data, many=True).data,
            "balance_sheet": BalanceSheetSerializer(bs_data, many=True).data
        })
    except DimCompany.DoesNotExist:
        return Response({"error": "Company not found"}, status=404)