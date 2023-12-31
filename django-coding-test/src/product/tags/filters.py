import datetime
from django import template
from django.template.defaultfilters import pluralize
from product.models import ProductVariant
from matplotlib.colors import is_color_like

register = template.Library()

@register.filter(name='get_product_variant_titles')
def get_product_variant_titles(args):
    titles = ProductVariant.objects.values_list('variant_title')
    # print(titles)
    size = []
    color = []
    for t in titles:
        # print(t)

        temp = ''
        for element in t:
            temp += str(element)
        # print(temp)
        string = temp.split('/')
        for s in string:
            # print(s)
            if is_color_like(s):
                # print('True')
                color.append(s)
            else:
                size.append(s)

    # print(color)
    # print(size)
    # print(color), print(size)
    if args.__eq__('color'):
        return color
    elif args.__eq__('size'):
        return size