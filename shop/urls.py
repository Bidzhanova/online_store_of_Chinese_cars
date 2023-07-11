from django.urls import path

from .views import (
    BrandsListView,
    BrandDetailsView,
    CarsListView,
    CarDetailsView,
)

app_name = 'shop'

urlpatterns = [
    path('brands/', BrandsListView.as_view(), name='brands'),
    path('brands/<int:pk>/', BrandDetailsView.as_view(), name='brand_details'),
    path('cars/', CarsListView.as_view(), name='cars'),
    path('cars/<int:pk>/', CarDetailsView.as_view(), name='car_details'),
]
