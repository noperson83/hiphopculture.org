from django.contrib import admin
from .models import Category, Product, Sale, Return, Receipt, RMA, Donation, Cart, CartItem, Size, ProductSize, ProductImage, PurchasedFrom, BusinessPurchase, BusinessPurchaseItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms for adding images

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'stock', 'quantity_purchased')
    list_filter = ('product', 'size')
    search_fields = ('product__name', 'size__name')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'size', 'quantity', 'total_price', 'sale_date')
    list_filter = ('sale_date', 'product')
    search_fields = ('user__username', 'product__name')

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('sale', 'reason', 'return_date')
    list_filter = ('return_date',)
    search_fields = ('sale__product__name', 'reason')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'receipt_number', 'total_amount', 'issued_date')
    list_filter = ('issued_date',)
    search_fields = ( 'receipt_number', 'user', 'issued_date')

@admin.register(RMA)
class RMAAdmin(admin.ModelAdmin):
    list_display = ('rma_number', 'return_entry', 'issued_date')
    search_fields = ('rma_number',)
    list_filter = ('issued_date',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for managing carts."""
    list_display = ('id', 'user', 'created_at', 'total_items')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

    def total_items(self, obj):
        """Calculate the total number of items in a cart."""
        return obj.items.count()
    total_items.short_description = 'Total Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin interface for managing cart items."""
    list_display = ('id', 'cart', 'product', 'quantity', 'size', 'price', 'total_price')
    list_filter = ('cart', 'product')
    search_fields = ('product__name', 'cart__user__username')

    def total_price(self, obj):
        """Calculate the total price for the cart item."""
        return obj.total_price
    total_price.short_description = 'Total Price'

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('user__username', 'product__name')

@admin.register(PurchasedFrom)
class PurchasedFromAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')

class BusinessPurchaseItemInline(admin.TabularInline):
    model = BusinessPurchaseItem
    extra = 1  # Number of empty forms for adding images

@admin.register(BusinessPurchase)
class BusinessPurchaseAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'purchased_from', 'purchase_total', 'purchase_date')
    filter_horizontal = ('product_sizes',)  # Optional for ManyToManyField
    inlines = [BusinessPurchaseItemInline]

@admin.register(BusinessPurchaseItem)
class BusinessPurchaseItemAdmin(admin.ModelAdmin):
    list_display = ('business_purchase', 'product_size', 'cost', 'quantity', 'total_cost')
