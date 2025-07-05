import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404, FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.core.mail import send_mail
from .models import Product, Category, Cart, CartItem, Size, ProductSize, Sale, Return, RMA, Receipt, Sale, BusinessPurchase, BusinessPurchaseItem
from .utils import SESSION_CART_KEY, get_session_cart, save_session_cart  # Updated import
from .forms import RMAForm

def download_digital_content(request, product_id):
    # Get the product and its digital content file
    product = get_object_or_404(Product, id=product_id)
    if not product.digital_content:
        raise Http404("Digital content not available.")

    # Stream the file to avoid memory errors
    file_path = product.digital_content.path
    response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{product.digital_content.name.split("/")[-1]}"'

    return response

def sales(request):
    sales = Sale.objects.all()
    total = 0
    for sale in sales:
        total += sale.total_price
    return render(request, 'shop/sales_list.html', {'sales': sales, 'total':total})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product_list.html', {'categories': categories, 'products': products, 'category': category})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_view(request):
    """Display the shopping cart and calculate shipping."""
    shipping_cost = request.session.get('shipping_cost', '0.00') 

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            total = Decimal('0.00')
            non_donation_items = [item for item in cart_items if not item.product.is_donation]
            total_non_donation_items = sum(item.quantity for item in non_donation_items)
            for item in cart_items:
                if item.product.is_donation:
                    total += item.price * item.quantity
                elif item.product.price:
                    total += item.product.price * item.quantity
        except Cart.DoesNotExist:
            cart_items = []
            total = Decimal('0.00')
            total_non_donation_items = 0

    else:  # Session cart
        session_cart = request.session.get('cart', {})
        cart_items = []
        total = Decimal('0.00')
        total_non_donation_items = 0
        for key, item_data in session_cart.items():
            product_id, type_str = key.split(":")
            product = get_object_or_404(Product, id=product_id)
            quantity = item_data.get("quantity", 0)
            if type_str == "donation":
                price_str = item_data.get('price', '0.00')
                product_size = 'Donation'
                try:
                    price = Decimal(price_str)
                except:
                    price = Decimal("0.00")
                total += price * quantity
                cart_items.append({"product": product, "quantity": quantity, "price": price, "key": key})
            else:
                size_id = int(type_str)
                size = get_object_or_404(Size, id=size_id)
                product_size = ProductSize.objects.get(product=product, size=size)
                if product.price:
                    total += product.price * quantity
                total_non_donation_items += quantity
                cart_items.append({"product": product, "quantity": quantity, "size": product_size, "key": key})
    
    order_id = f"THX-{uuid.uuid4().hex[:12]}"  # Example: ORD-a6331b496b79
    request.session['order_id'] = order_id
    request.session['total'] = float(total)
    request.session['shipping_cost'] = shipping_cost

    return render(request, 'shop/cart.html', {
        'cart': cart if request.user.is_authenticated else None,
        'cart_items': cart_items,
        'shipping_cost': shipping_cost,  # Pass shipping_cost to the template
        'total': total,
        'order_id': order_id,
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        if product.is_donation:
            try:
                price = Decimal(request.POST.get('price'))
                if price <= 0:
                    raise ValueError("Donation must be greater than 0")
            except (TypeError, ValueError):
                messages.error(request, "Invalid donation amount.")
                return redirect(request.META.get('HTTP_REFERER'))

            size = None
        else:
            size_id = request.POST.get('size')
            size = get_object_or_404(Size, id=size_id)
            product_size = get_object_or_404(ProductSize, product=product, size=size)
            if product_size.stock < 1:
                messages.error(request, f"Sorry, {product.name} in {size.name} is out of stock!")
                return redirect(request.META.get('HTTP_REFERER'))
            
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
            if product.is_donation:
                cart_item.price = price
                cart_item.size = size
            elif not created:
                cart_item.quantity += 1
                cart_item.size = size
            cart_item.save()

        else:  # Session-based cart
            session_cart = request.session.get('cart', {})  # Get or create
            key = f"{product.id}:donation" if product.is_donation else f"{product.id}:{size.id}"
            item_data = session_cart.get(key, {'quantity': 0})
            item_data['quantity'] += 1
            if product.is_donation:
                item_data['price'] = str(price) # Store price as string in session
            session_cart[key] = item_data
            request.session['cart'] = session_cart # Save the updated cart to the session

        destination = request.POST.get('destination', 'USA')

        # Calculate the total number of *non-donation* items in the cart
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            total_items = sum(item.quantity for item in cart.items.all() if not item.product.is_donation and not item.product.is_noshipping)
        else:
            session_cart = request.session.get('cart', {})
            total_items = sum(details if isinstance(details, int) else details.get('quantity', 0) for key, details in session_cart.items() if not Product.objects.get(id=key.split(":")[0]).is_donation and not Product.objects.get(id=key.split(":")[0]).is_noshipping)

        base_rate = 7.50
        additional_rate = 2.50

        shipping_cost = 0.0

        if total_items > 0: #only calculate if there are non donation items
            if destination == "USA":
                shipping_cost = base_rate + (total_items - 1) * additional_rate
            elif destination == "International":
                base_rate = 23.00
                additional_rate = 5.00
                shipping_cost = base_rate + (total_items - 1) * additional_rate

        # ... (rest of the code for saving shipping cost and redirecting)
        if request.user.is_authenticated:
            cart.shipping_cost = Decimal(shipping_cost)
            cart.save()
        else:
            request.session['shipping_cost'] = shipping_cost

        messages.success(request, f"Shipping updated to {destination} with cost ${shipping_cost:.2f}")
    return redirect('shop:cart_view')

def remove_from_cart(request, item_key):
    """Remove an item from the cart and replenish the stock."""
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                cart_item = CartItem.objects.get(id=item_key, cart__user=request.user)
                # Remove the cart item
                cart_item.delete()
            except (CartItem.DoesNotExist, ProductSize.DoesNotExist):
                raise Http404("Cart item or product size not found.")
        else:
            if ":" in item_key:
                product_id, size_id = item_key.split(":")
                session_cart = get_session_cart(request)

                if item_key in session_cart:
                    quantity = session_cart[item_key].get('quantity', 0) 

                    # Replenish stock
                    product = get_object_or_404(Product, id=product_id)
                    if size_id != "donation":
                        size = get_object_or_404(Size, id=size_id)
                        product_size = ProductSize.objects.get(product=product, size=size)
                        product_size.stock += quantity
                        product_size.save()
                    
                    del session_cart[item_key]
                    save_session_cart(request, session_cart)
                else:
                    raise Http404("Cart item not found in session cart.")
            else:
                raise ValueError("Invalid item key format.")

        destination = request.POST.get('destination', 'USA')

        # Calculate the total number of *non-donation* items in the cart
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            total_items = sum(item.quantity for item in cart.items.all() if not item.product.is_donation and not item.product.is_noshipping)
        else:
            session_cart = request.session.get('cart', {})
            total_items = sum(details if isinstance(details, int) else details.get('quantity', 0) for key, details in session_cart.items() if not Product.objects.get(id=key.split(":")[0]).is_donation and not Product.objects.get(id=key.split(":")[0]).is_noshipping)

        base_rate = 7.50
        additional_rate = 2.50

        shipping_cost = 0.0

        if total_items > 0: #only calculate if there are non donation items
            if destination == "USA":
                shipping_cost = base_rate + (total_items - 1) * additional_rate
            elif destination == "International":
                base_rate = 23.00
                additional_rate = 5.00
                shipping_cost = base_rate + (total_items - 1) * additional_rate

        # ... (rest of the code for saving shipping cost and redirecting)
        if request.user.is_authenticated:
            cart.shipping_cost = shipping_cost
            cart.save()
        else:
            request.session['shipping_cost'] = shipping_cost

        messages.success(request, f"Shipping updated to {destination} with cost ${shipping_cost:.2f}")

    return redirect('shop:cart_view')

def adjust_stock(product, size, quantity):
    """Helper function to adjust stock for a product and size."""
    try:
        product_size = ProductSize.objects.get(product=product, size=size)
        if product_size.stock < quantity:
            raise Http404(f"Insufficient stock for {product.name} (Size: {size.name}).")
        product_size.stock -= quantity
        product_size.save()
    except ProductSize.DoesNotExist:
        raise Http404(f"Size not available for {product.name}.")
    
def purchase_success(request):
    """Render purchase success page."""
    # Create a receipt entry
    receipt_number = request.session.get('order_id', 'THX-xxxxxxxxxxxx')
    shipping_cost = request.session.get('shipping_cost', '0.00') 
    total_amount = request.session.get('total', '101.00')
    # Initialize an empty list to store Sale objects
    sales = []

    if request.user.is_authenticated:
        # Process cart for authenticated users
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        for item in cart_items:
            if item.product.is_donation:
                total = item.price
                product_size = 'Donation'
                size= None
                try:
                    total_price = Decimal(total)
                except:
                    total_price = Decimal("0.00")
            else:
                # Adjust stock
                adjust_stock(item.product, item.size, item.quantity)
                total_price=item.quantity * item.product.price
            # Create a Sale object and add it to the list
            sale = Sale.objects.create(
                user=request.user if request.user.is_authenticated else None,
                product=item.product,
                size=item.size,
                quantity=item.quantity,
                total_price=total_price
            )
            sales.append(sale)  # Ensure we append Sale objects, not CartItems
        shipping_cost = cart.shipping_cost
        # Clear cart
        cart_items.delete()
    else:
        # Process cart for non-authenticated users
        session_cart = get_session_cart(request)
        for key, details in session_cart.items():
            product_id, size_id = key.split(":") if ":" in key else (key, None)
            product = Product.objects.get(id=product_id)
            if size_id == "donation":
                price_str = details.get('price', '0.00')
                product_size = 'Donation'
                size= None
                try:
                    total_price = Decimal(price_str)
                except:
                    total_price = Decimal("0.00")
            else:
                size_id = int(size_id)
                size = get_object_or_404(Size, id=size_id)
                total_price=details['quantity'] * product.price
            # Adjust stock
            if not product.is_donation:
                product_size = ProductSize.objects.get(product=product, size=size)
                product_size.stock -= details['quantity']
                product_size.save()

            # Create a Sale object and add it to the list
            sale = Sale.objects.create(
                product=product,
                size=size,
                quantity=details['quantity'],
                total_price=total_price
            )
            sales.append(sale)  # Ensure we append Sale objects, not session cart items
        # Clear session cart
        del request.session[SESSION_CART_KEY]
        request.session.modified = True

    # Generate a receipt
    receipt = Receipt.objects.create(
        user = request.user if request.user.is_authenticated else None,
        receipt_number = receipt_number,
        total_amount = total_amount + float(shipping_cost)
    )
    receipt.sales.set(sales)

    return render(request, 'shop/success.html', {'receipt': receipt, 'shipping_cost': shipping_cost})

def send_receipt_email(receipt):
    subject = f"Your Receipt #{receipt.receipt_number}"
    message = f"Thank you for your purchase! Your receipt total is ${receipt.total_amount}."
    recipient = receipt.user.email if receipt.user else None

    if recipient:
        send_mail(
            subject,
            message,
            'marcus@noperson.com',  # Sender's email
            [recipient],
            fail_silently=False,
        )

def request_rma(request, sale_id):
    """Handle RMA requests."""
    sale = get_object_or_404(Sale, id=sale_id)

    if request.method == 'POST':
        form = RMAForm(request.POST)
        if form.is_valid():
            return_entry = Return.objects.create(
                sale=sale,
                reason=form.cleaned_data['reason']
            )
            RMA.objects

def donation_page(request, slug):
    product = get_object_or_404(Product, slug=slug, is_donation=True)
    return render(request, 'shop/donation_page.html', {'product': product})

def finance_dashboard(request):
    purchases = BusinessPurchase.objects.all().all()
    total_p = sum(purchase.purchase_total for purchase in purchases)
    inventories = BusinessPurchaseItem.objects.all().order_by(
        'product_size__product__name',  # Sort by product name
        'product_size__size__name'     # Then by size name
        )
    total_c = sum(inventory.total_cost for inventory in inventories)
    total_m = sum(inventory.total_make for inventory in inventories)
    sales = Sale.objects.all().order_by(
        'product__name',  # Sort by product name
        'size__name'     # Then by size name
        )
    total_revenue = sum(sale.total_price for sale in sales)
    total_profit = sum(sale.profit for sale in sales)

    context = {
        'purchases': purchases,
        'total_p': total_p,
        'inventories': inventories,
        'total_c': total_c,
        'total_m': total_m,
        'sales': sales,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
    }
    return render(request, 'shop/finance_dashboard.html', context)
