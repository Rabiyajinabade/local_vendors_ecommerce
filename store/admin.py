from django.contrib import admin
from .models import Vendor, Product, Order

class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop_name', 'description')
    fields = ('user', 'shop_name', 'description')

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product)
admin.site.register(Order)
