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
        # 1. Fetch data inside the 'try' block
        profile = DimCompany.objects.get(symbol=symbol)
        pl_data = FactProfitLoss.objects.filter(symbol=symbol)
        bs_data = FactBalanceSheet.objects.filter(symbol=symbol)

        # 2. Return the success response
        return Response({
            "profile": CompanySerializer(profile).data,
            "profit_loss": ProfitLossSerializer(pl_data, many=True).data,
            "balance_sheet": BalanceSheetSerializer(bs_data, many=True).data,
        })
        
    except DimCompany.DoesNotExist:
        # 3. Handle the case where the company isn't found
        return Response({"error": "Company not found"}, status=404)