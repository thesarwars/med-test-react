from django.views import generic

from product.models import Variant, Product, ProductVariantPrice, ProductVariant
from product.forms import CreateProd
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.db.models import Q


@method_decorator(csrf_exempt, name='dispatch')
class CreateProductView(generic.TemplateView):
    form_class = CreateProd
    # model = Product
    template_name = 'products/create.html'
    success_url = '/product/create'
    
    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        
        if form.is_valid():
            # Process the form data and save to the database
            title = form.cleaned_data['title']
            sku = form.cleaned_data['sku']
            description = form.cleaned_data['description']
            # save = Product.objects.create(title=title, sku=sku, description=description)
            # Save the data to the Product model or perform other actions
            Product.objects.create(title=title, sku=sku, description=description)
            # success_url = reverse('list.product')
            # Redirect to a success page or another URL
            return redirect('success_url')
            # return save

        # If the form is not valid, re-render the form with errors
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context = {'product': True, 'variants': list(variants.all()), 'form': form}
        return render(request, self.template_name, context)
    

class ProductListView(generic.ListView):
    model = ProductVariantPrice
    template_name = 'products/list.html'
    context_object_name = 'product_variant_prices'
    paginate_by = 2
    queryset = ProductVariantPrice.objects.all()
    

class ProductVariantView(generic.ListView):
    model = ProductVariant
    template_name = 'products/list.html'
    context_object_name = 'product_variant'
    # paginate_by = 2
    queryset = ProductVariant.objects.all()
    print(queryset)
    
    
def filtering(request):
    qs = ProductVariantPrice.objects.all()
    
    title = request.GET.get('title')
    variant = request.GET.get('variant')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    date = request.GET.get('date')
    
    if title != '' and title is not None:
        qs = qs.filter(product__title__icontains=title)
        
    if variant and variant != '--Select A Variant--':
        qs = qs.filter(
            Q(product_variant_one__variant_title__icontains=variant) |
            Q(product_variant_two__variant_title__icontains=variant) |
            Q(product_variant_three__variant_title__icontains=variant)
        )
        
    if price_from:
        qs = qs.filter(price__gte=price_from)
        
    if price_to:
        qs = qs.filter(price__gte=price_to)
        
    if date:
        qs = qs.filter(product__created_at__gte=date)
        
    return render(request, 'products/list.html', {'product_variant_prices': qs})