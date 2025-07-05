SESSION_CART_KEY = 'cart'  # Key for storing the cart in the session

def get_session_cart(request):
    """Retrieve or initialize the session cart."""
    cart = request.session.get(SESSION_CART_KEY, {})
    if not isinstance(cart, dict):  # Ensure it is a dictionary
        cart = {}
    return cart

def save_session_cart(request, cart):
    """Save the cart back into the session."""
    request.session[SESSION_CART_KEY] = cart
    request.session.modified = True
