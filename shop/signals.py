from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem, Product
from .utils import get_session_cart, save_session_cart

@receiver(user_logged_in)
def merge_carts(sender, request, user, **kwargs):
    """Merge session cart into authenticated user's cart on login."""
    session_cart = get_session_cart(request)
    if session_cart:
        cart, created = Cart.objects.get_or_create(user=user)
        for product_id, quantity in session_cart.items():
            product = Product.objects.get(id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        # Clear session cart
        save_session_cart(request, {})
