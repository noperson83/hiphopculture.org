from django.db import models
from django.conf import settings
import os

class Sale(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # Use settings.AUTH_USER_MODEL for the user relation
        on_delete=models.CASCADE,   # Allows setting to NULL if the related user is deleted
        null=True,                  # Allows NULL values in the database
        blank=True                  # Optional in forms
    )
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.ForeignKey('Size', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.ForeignKey('ProductSize', on_delete=models.CASCADE, null=True, blank=True)
    sale_date = models.DateTimeField(auto_now_add=True)

    @property
    def profit(self):
        """Calculate profit for this sale."""
        if self.inventory:
            # Get the related BusinessPurchaseItem
            purchase_item = BusinessPurchaseItem.objects.filter(
                product_size=self.inventory
            ).first()

            if not purchase_item:
                # Fallback or handle the missing data
                return 0  # No profit calculation possible without cost data

            # Calculate the cost price using the BusinessPurchaseItem cost
            cost_price = self.quantity * purchase_item.cost
            return self.total_price - cost_price - (self.shipping_cost or 0)
        return 0

    def __str__(self):
        user_display = self.user.email if self.user else "Anonymous"
        return f"{user_display} - {self.product.name} ({self.size.name}) - {self.quantity}"

class Receipt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use settings.AUTH_USER_MODEL for the user relation
        on_delete=models.CASCADE,
        null=True,                  # Allows NULL values in the database
        blank=True                  # Optional in forms
    )
    sales = models.ManyToManyField('Sale')  # Associate multiple sales with one receipt
    receipt_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.receipt_number}"

class Return(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='returns')
    reason = models.TextField()
    return_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return for {self.sale.product.name}"

class RMA(models.Model):
    return_entry = models.OneToOneField(Return, on_delete=models.CASCADE, related_name='rma')
    rma_number = models.CharField(max_length=20, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RMA #{self.rma_number}"

def upload_to_product_folder(instance, filename):
    # Normalize the product name to be used as a folder name
    product_name = instance.name.replace(' ', '_').lower()
    folder_name = f'media/{product_name}/'
    return os.path.join(folder_name, filename)

class SizeCategory(models.TextChoices):
    """Size categories for different target audiences."""
    MASCULINE = 'M', 'Masculine'
    FEMININE = 'F', 'Feminine'
    CHILD = 'C', 'Child'

class Size(models.Model):
    """Sizes available for products."""
    name = models.CharField(max_length=10)  # e.g., XS, S, M, L, XL
    category = models.CharField(
        max_length=1,
        choices=SizeCategory.choices,
        default=SizeCategory.MASCULINE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Category(models.Model):
    """Categories for products."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class ProductSize(models.Model):
    """Intermediate model to manage sizes and quantities for products."""
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_sizes')
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)  # Quantity available for this size
    quantity_purchased = models.PositiveIntegerField(default=0)  # Correct field type

    def __str__(self):
        return f"{self.product.name} - {self.size.name} (Stock: {self.stock})"

class Product(models.Model):
    """General product model."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    digital_content = models.FileField(upload_to=upload_to_product_folder, blank=True, null=True)
    is_donation = models.BooleanField(default=False)  # For donation-based products
    is_noshipping = models.BooleanField(default=False)  # For no shipping products
    image = models.ImageField(upload_to=upload_to_product_folder, blank=True, null=True)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    """Additional images for a product."""
    name = models.CharField(max_length=200, blank=True)  # Leave blank if dynamically set
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_to_product_folder)

    def __str__(self):
        return f"Image for {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Automatically set the name if not provided
        if not self.name:
            self.name = f"Image for {self.product.name}"
        super().save(*args, **kwargs)

class Donation(models.Model):
    """Track donations for digital content."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use settings.AUTH_USER_MODEL for the user relation
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        limit_choices_to={'is_donation': True}
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.amount}"

class Cart(models.Model):
    """Shopping cart model to track items per user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        null=True,
        blank=True
    )
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({self.id}) - User: {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey('Size', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    @property
    def total_price(self):
        total=0
        if self.product.is_donation:
            total += self.price
        elif self.product.price:
            total += self.product.price * self.quantity
        return total
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
class PurchasedFrom(models.Model):
    """Represents a vendor or supplier from whom products are purchased."""
    name = models.CharField(max_length=255)
    contact_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class BusinessPurchase(models.Model):
    """Represents a business purchase with an invoice."""
    invoice_number = models.CharField(max_length=50, unique=True)
    purchased_from = models.ForeignKey(PurchasedFrom, on_delete=models.CASCADE, related_name='purchases')
    product_sizes = models.ManyToManyField(
        ProductSize,
        through='BusinessPurchaseItem',
        related_name='business_purchases'
    )
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    purchase_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    purchase_date = models.DateField(auto_now_add=True)

    def calculate_total(self):
        """Calculate the total cost of all product sizes plus tax and shipping."""
        items_total = sum(
            item.total_cost for item in self.businesspurchaseitem_set.all()
        )
        self.purchase_total = items_total + self.tax + self.shipping

    def save(self, *args, **kwargs):
        self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.invoice_number} from {self.purchased_from.name}"
    
class BusinessPurchaseItem(models.Model):
    """Intermediate model to track quantities and costs per ProductSize in a BusinessPurchase."""
    business_purchase = models.ForeignKey(BusinessPurchase, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    total_make = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)

    def save(self, *args, **kwargs):
        """Calculate total cost based on quantity and product size cost per item."""
        self.total_cost = self.quantity * self.cost
        self.total_make = self.product_size.quantity_purchased * self.product_size.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product_size} for {self.business_purchase}"


