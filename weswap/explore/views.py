# explore/views.py

from django.shortcuts import render
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