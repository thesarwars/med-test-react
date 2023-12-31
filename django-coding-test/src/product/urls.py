from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView, ProductListView, filtering, ProductVariantView
from product.views.variant import VariantView, VariantCreateView, VariantEditView
from product.models import ProductVariantPrice, ProductVariant

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', ProductListView.as_view(template_name='products/list.html', extra_context={
        'product': True,
        # 'product_variant_prices': ProductVariantPrice.objects.all(),
        # 'product_variant': ProductVariantView.as_view()
    }), name='list.product'),
    
    path('filter/', filtering, name='list_filtered'),
    # path('color/', ProductVariantView.as_view(), name='product_variant'),
    path('color/', ProductVariantView.as_view(template_name='products/list.html', extra_context={
        'product': True,
    }), name='product_variant'),
]
