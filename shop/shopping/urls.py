from django.urls import path
from shopping.views import AddressDetailAPIView, AddressListCreateAPIView

urlpatterns = [
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),
]