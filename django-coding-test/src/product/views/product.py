from django.views import generic

from product.models import Variant, Product
from product.forms import CreateProd
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect



@method_decorator(csrf_exempt, name='dispatch')
class CreateProductView(generic.TemplateView):
    form_class = CreateProd
    # model = Product
    template_name = 'products/create.html'
    success_url = '/product/list'
    
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

            # Save the data to the Product model or perform other actions
            Product.objects.create(title=title, sku=sku, description=description)

            # Redirect to a success page or another URL
            return redirect('success_url')

        # If the form is not valid, re-render the form with errors
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context = {'product': True, 'variants': list(variants.all()), 'form': form}
        return render(request, self.template_name, context)