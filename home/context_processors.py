from .models import SiteSettings
from shop.models import Cart
from shop.utils import get_session_cart

def cart_context(request):
    """Add cart data to the context."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return {'cart': cart, 'session_cart': None}
    else:
        session_cart = get_session_cart(request)

        # Ensure session_cart is a dictionary
        if not isinstance(session_cart, dict):
            session_cart = {}

        return {
            'cart': None,
            'session_cart': {
                'items': session_cart,
            }
        }

def global_context(request):
    settings = SiteSettings.objects.first()
    return {
        'site_promotion': settings.promotion_message if settings else "Default Promotion",
        'active_trend': settings.active_trend if settings else "Default Trend",
    }
