from django.contrib import admin

from .models import Brand, Car, CarImage


class CarInline(admin.TabularInline):
    model = Car

class CarImageInline(admin.TabularInline):
    model = CarImage

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines = [
        CarInline,
    ]
    list_display = ('pk', 'title', 'brand_country', 'image', 'description_short', 'created_at')
    list_display_links = ('pk', 'title')
    ordering = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)

    def description_short(self, brand: Brand) -> str:
        if len(brand.description) < 50:
            return brand.description
        return brand.description[:50] + '...'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [
        CarImageInline,
    ]

    list_display = (
        'pk', 'brand', 'model', 'preview', 'price', 'discount', 'created_at',
    )
    list_display_links = ('pk', 'model',)
    list_filter = ('model',  'car_class', 'doors_qty', 'seats_qty', 'transmission', 'drive',)
    search_fields = ('model',)
    fieldsets = [
        ('Общая информация', {
            'fields': ('brand', 'model', 'car_class', 'doors_qty', 'seats_qty', 'engine_power',
                       'engine_capacity', 'consumption', 'max_speed',),
        }),
        ('Превью', {
            'fields': ('preview',),
        }),
        ('Объём', {
           'fields': ('trunk_volume', 'fuel_tank_capacity',) ,
        }),
        ('Трансмиссия', {
            'fields': ('transmission', 'drive',),
        }),
        ('Цена', {
            'fields': ('price', 'discount',),
        }),
    ]

    def get_queryset(self, request):
        return Car.objects.select_related('brand')
