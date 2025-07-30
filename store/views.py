from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count

from .models import Product, Vendor, OrderItem,Order
from .utils import get_conversion_rate

# ---------------------------------------------
# 🏠 Home Page: Shows all products with USD conversion
# ---------------------------------,------------
def home(request):
    products = Product.objects.all()
    conversion_rate = get_conversion_rate('INR', 'USD')  # Convert INR → USD

    for product in products:
        if conversion_rate:
            product.usd_price = round(product.price * conversion_rate, 2)
        else:
            product.usd_price = "Conversion Failed"

    return render(request, 'store/home.html', {'products': products})


# ---------------------------------------------
# 📦 Product Detail Page
# ---------------------------------------------
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


# ---------------------------------------------
# 🧑‍💼 Vendor Detail Page
# ---------------------------------------------
def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    products = vendor.product_set.all()
    return render(request, 'store/vendor_detail.html', {
        'vendor': vendor,
        'products': products
    })


# ---------------------------------------------
# ➕ Add Product to Cart
# ---------------------------------------------
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('view_cart')


# ---------------------------------------------
# 🛒 View Cart
# ---------------------------------------------
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


# ---------------------------------------------
# ❌ Remove from Cart
# ---------------------------------------------
@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')


# ---------------------------------------------
# ✅ Checkout (Clears the cart)
# ---------------------------------------------
def checkout(request):
    request.session['cart'] = {}
    return render(request, 'store/checkout.html')


# ---------------------------------------------
# 📊 Sales Report (Shreedar’s module)
# ---------------------------------------------
def sales_report(request):
    total_orders = OrderItem.objects.count()

    total_revenue = OrderItem.objects.aggregate(
        total=Sum('product__price')
    )['total'] or 0

    top_products = (
        OrderItem.objects
        .values('product__name')
        .annotate(quantity_sold=Count('id'))
        .order_by('-quantity_sold')[:5]
    )

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'top_products': top_products,
    }
    return render(request, 'store/report.html', context)
