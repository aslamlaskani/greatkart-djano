from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from .models import Cart, CartItem

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart

def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_items = CartItem.objects.filter(product=product, cart=cart)

        ex_var_list = []
        id_list = []

        for item in cart_items:
            existing_variation = list(item.variations.all())
            ex_var_list.append(existing_variation)
            id_list.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id_list[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if product_variation:
                item.variations.set(product_variation)
            item.save()
    else:
        item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if product_variation:
            item.variations.set(product_variation)
        item.save()

    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        # Get only the first matching CartItem and delete it
        cart_item = CartItem.objects.filter(product=product, cart=cart).first()
        if cart_item:
            cart_item.delete()
    except:
        pass

    return redirect('cart')

def cart(request):
    total = 0
    quantity = 0
    tax = 0
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
          total += cart_item.sub_total()


        tax = round((2 * total) / 100, 2)
        grand_total = round(total + tax, 2)

    except ObjectDoesNotExist:
        cart_items = []

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)
