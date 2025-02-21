from django.shortcuts import render
from rest_framework.views import APIView
from shopping.models import Address
from shopping.serializers import AddressSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import OpenApiParameter, extend_schema

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

    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            return None

    def get(self, request, pk):
        address = self.get_object(pk)
        if address is None:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddressSerializer(address)
        return Response(serializer.data)


    def delete(self, request, pk):
        address = self.get_object(pk)
        if address is None:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response({"message": "Address deleted"}, status=status.HTTP_204_NO_CONTENT)
