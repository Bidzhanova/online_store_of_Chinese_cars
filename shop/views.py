from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Brand, Car, CarImage


class BrandsListView(ListView):
    model = Brand
    template_name = 'shop/brands.html'
    context_object_name = 'brands'

class BrandDetailsView(DetailView):
    model = Brand
    template_name = 'shop/brand_details.html'
    context_object_name = 'brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.filter(brand=self.object).all()
        return context

class CarsListView(ListView):
    queryset = Car.objects.select_related('brand')
    template_name = 'shop/cars.html'
    context_object_name = 'cars'

class CarDetailsView(DetailView):
    model = Car
    template_name = 'shop/car_details.html'
    context_object_name = 'car'
