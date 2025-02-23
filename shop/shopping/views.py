from django.shortcuts import render
from rest_framework.views import APIView
from shopping.models import Address, User, Supplier
from shopping.serializers import AddressSerializer, LoginSerializer, RegisterSerializer, SupplierSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiParameter
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password



# Create your views here.

class AddressListCreateAPIView(APIView):

    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    @extend_schema(
            summary='Address',
            description='Enter address',
            request=AddressSerializer
    )

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AddressDetailAPIView(APIView):

    def get(self, request, pk):
        address = Address.objects.get(pk=pk)
        if not address:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address)
        return Response(serializer.data)


    def delete(self, request, pk):
        address = Address.objects.get(pk=pk)
        if address is None:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response({"message": "Address deleted"}, status=status.HTTP_204_NO_CONTENT)

class LoginAPIView(APIView):
    @extend_schema(
            summary='User Login',
            description='Login using email and password to obtain JWT tokens',
            request=LoginSerializer,
            responses={
                200: OpenApiParameter(name='Tokens', description='JWT access and refresh tokens'),
                400: OpenApiParameter(name='Errors', description='Invalid credentials or validation errors')
            },
            tags=['User Authentication']
    )
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = User.objects.get(email = email)
            if user.check_password(password):
                if not user.is_active :
                    return Response({'detail': 'User is anactive'}, status=status.HTTP_400_BAD_REQUEST)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    'refresh': str(refresh),
                    'access': access_token
                }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):
    @extend_schema(
        summary='User Register',
        description='Register using email and password to obtain JWT tokens',
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="JWT access and refresh tokens"),
            400: OpenApiResponse(description="Invalid credentials or validation errors"),
        },
        tags=['User Authentication']
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)  # 🔍 DEBUG
            if 'password' not in serializer.validated_data:
                return Response({"error": "Password field is missing"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = serializer.save()
                user.set_password(serializer.validated_data['password'])
                user.save()

                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': RegisterSerializer(user).data
                    }, status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuplierCreateAPIView(APIView):
    def get(self, request):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    @extend_schema(
            summary='Supplier',
            description='Enter supplier',
            request=SupplierSerializer
    )

    def post(self, request):
        serializer = SupplierSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuplierDetailAPIView(APIView):
    def get(self, request, user_id, pk):
        try:
            supplier = Supplier.objects.get(user_id=user_id, pk=pk)
        except Supplier.DoesNotExist:
            return Response({'error': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    def delete(self, request, user_id, pk):
        try:
            supplier = Supplier.objects.get(user_id=user_id, pk=pk)
        except Supplier.DoesNotExist:
            return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)
        
        supplier.delete()
        return Response({"message": "Supplier deleted"}, status=status.HTTP_204_NO_CONTENT)

