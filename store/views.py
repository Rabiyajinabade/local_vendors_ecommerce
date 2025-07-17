
# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Vendor, Product

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    products = Product.objects.filter(vendor=vendor)
    return render(request, 'store/vendor_detail.html', {
        'vendor': vendor,
        'products': products
    })
