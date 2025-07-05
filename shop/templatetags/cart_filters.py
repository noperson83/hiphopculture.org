from django import template
from shop.models import Product, Size
register = template.Library()

@register.filter
def lookup_product(product_id):
    return Product.objects.get(id=product_id)

@register.filter
def cart_total(cart_items):
    if isinstance(cart_items, dict):  # Session-based cart
        # Ensure valid data structure
        total = sum(
            item['price'] * item['quantity']
            for item in cart_items.values()
            if isinstance(item, dict) and 'price' in item and 'quantity' in item
        )
        return total
    elif hasattr(cart_items, 'all'):  # Model-based cart
        total = 0
        for item in cart_items:
            if item.product.is_donation:
                total += item.price
            elif item.product.price:
                total += item.product.price * item.quantity
        return total

@register.filter
def split(value, delimiter=":"):
    """
    Split the string by the given delimiter.
    Default delimiter is ':'.
    """
    if isinstance(value, str):
        return value.split(delimiter)
    return value

@register.filter
def lookup_product_name(product_id):
    """Get the product name by ID."""
    try:
        return Product.objects.get(id=product_id).name
    except Product.DoesNotExist:
        return "Unknown Product"
    
@register.filter
def lookup_product_image(product_id):
    """Get the product name by ID."""
    try:
        return Product.objects.get(id=product_id).image.url
    except Product.DoesNotExist:
        return "Unknown Product"

@register.filter
def lookup_product_price(product_id):
    """Get the product price by ID."""
    try:
        return Product.objects.get(id=product_id).price
    except Product.DoesNotExist:
        return 0.0

@register.filter
def lookup_size_name(size_id):
    """Get the size name by ID."""
    try:
        return Size.objects.get(id=size_id).name
    except Size.DoesNotExist:
        return "Unknown Size"

@register.filter
def multiply(value, multiplier):
    """Multiply two values."""
    return value * multiplier
