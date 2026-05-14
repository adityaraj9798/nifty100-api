from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DimCompany, FactProfitLoss, FactBalanceSheet
from .serializers import CompanySerializer, ProfitLossSerializer, BalanceSheetSerializer

# --- EXISTING VIEWS ---

@api_view(['GET'])
def get_companies(request):
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
        profile = DimCompany.objects.get(symbol=symbol)
        pl_data = FactProfitLoss.objects.filter(symbol=symbol)
        bs_data = FactBalanceSheet.objects.filter(symbol=symbol)

        return Response({
            "profile": CompanySerializer(profile).data,
            "profit_loss": ProfitLossSerializer(pl_data, many=True).data,
            "balance_sheet": BalanceSheetSerializer(bs_data, many=True).data,
        })
    except DimCompany.DoesNotExist:
        return Response({"error": "Company not found"}, status=404)

# --- NEW REGISTRATION VIEW (REQUIRED FOR PORTAL) ---

@api_view(['POST'])
def register_business(request):
    """
    Handles B2B Portal Registration.
    Matches the frontend call to: /api/register/
    """
    email = request.data.get('email')
    business_name = request.data.get('businessName')

    if not email or not business_name:
        return Response({"error": "Email and Business Name are required"}, status=status.HTTP_400_BAD_REQUEST)

    # For now, we return a success response so your frontend can proceed.
    # If you have a Business model, you would do Business.objects.create() here.
    return Response({
        "message": "Registration successful",
        "user": {
            "id": 101,  # Mock ID to let the frontend move to the next step
            "email": email,
            "businessName": business_name
        }
    }, status=status.HTTP_201_CREATED)