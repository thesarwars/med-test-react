import datetime
from django import template
from django.template.defaultfilters import pluralize
from product.models import ProductVariant
from matplotlib.colors import is_color_like

register = template.Library()


# @register.filter(name='passed_time')
# def passed_time(time):
#     time = str(time).split('+', 2)[0]
#     created_at = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

#     current_time = datetime.datetime.now()
#     current_time = str(current_time).split('.', 2)[0]
#     current_time = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
#     passed_time = current_time - created_at
#     total_seconds = passed_time.total_seconds()
#     day = int(total_seconds // 86400)
#     remaining_hours_in_seconds = total_seconds % 86400
#     hour = int(remaining_hours_in_seconds // 3600)
#     return 'Created at: {} day{} and {} hour{} ago'.format(day, pluralize(day), hour, pluralize(hour))


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