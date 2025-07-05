from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='shop'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('donate/<slug:slug>/', views.donation_page, name='donation_page'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<str:item_key>/', views.remove_from_cart, name='remove_from_cart'),
    path('purchase-success/', views.purchase_success, name='purchase_success'),
    path('request-rma/<int:sale_id>/', views.request_rma, name='request_rma'),
    path('sales/', views.sales, name='sales'),
    path('download/<int:product_id>/', views.download_digital_content, name='download_digital_content'),
    path('finance/', views.finance_dashboard, name='finance_dashboard'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)