
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Vendor
from django.views.decorators.http import require_POST

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})



def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    products = vendor.product_set.all()
    return render(request, 'store/vendor_detail.html', {
        'vendor': vendor,
        'products': products
    })



# 1. Add product to cart

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    request.session.modified = True  # 🟢 Ensures session is saved

    print("Cart:", cart)  # DEBUG: Check in terminal

    return redirect('view_cart')



# 2. View cart
def view_cart(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    
    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })


    return render(request, 'store/view_cart.html', {
    'cart_items': cart_items,
    'total': total,



    })




# 3. Remove item from cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')

# 4. Dummy Checkout (just clear the cart)
def checkout(request):
    request.session['cart'] = {}
    return render(request, 'store/checkout.html')

