# explore/views.py

from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    # Fetch distinct categories from the Product model
    categories = Product.objects.values_list('category', flat=True).distinct()
    return render(request, 'explore/base.html', {'categories': categories})

def subcategories(request, category):
    # Fetch distinct subcategories based on the selected category
    subcategories = Product.objects.filter(category=category).values_list('sub_category', flat=True).distinct()
    return render(request, 'explore/sub-categories.html', {'category': category, 'subcategories': subcategories})
def base(request):
    # You may need to pass categories to the template if required
    # Example: categories = ['Category1', 'Category2']
    return render(request, 'explore/base.html', {})

def discovery(request):
    subcategory = request.GET.get('subcategory')
    if subcategory:
        products = Product.objects.filter(sub_category=subcategory)
    else:
        products = Product.objects.all()  # Show all products if no filter is applied

    return render(request, 'explore/discovery.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'explore/product_detail.html', {'product': product})