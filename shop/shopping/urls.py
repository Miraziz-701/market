from django.urls import path
from shopping.views import AddressDetailAPIView, AddressListCreateAPIView, RegisterAPIView, LoginAPIView, SuplierDetailAPIView, SuplierCreateAPIView

urlpatterns = [
    path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('supplier/<int:pk>/', SuplierDetailAPIView.as_view(), name='supplier-detail'),
    path('supplier/', SuplierCreateAPIView.as_view(), name='supplier-create')
]