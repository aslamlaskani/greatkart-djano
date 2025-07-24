from .models import Cart, CartItem
from .views import _cart_id  # Fixed double underscore

def counter(request):
    cart_count = 0
    if 'admin' in request.path:  # Fixed syntax
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()  # Use .first() to get one cart object
            if cart:
                cart_items = CartItem.objects.filter(cart=cart)  # Correct model name and usage
                for cart_item in cart_items:  # Fixed syntax
                    cart_count += cart_item.quantity
        except Cart.DoesNotExist:  # Technically not raised by .filter(), but keeping as you have it
            cart_count = 0

        return dict(cart_count=cart_count)  # Always return a context dictionary
