# explore/views.py

from django.shortcuts import render, get_object_or_404
from .models import Product, ProductImage
from django.contrib.auth.decorators import login_required
# explore/views.py


from django.utils import timezone
from datetime import timedelta

from django.shortcuts import render
from .models import Product, ProductImage

from explore.models import Product, ProductImage


def home(request):
    categories = Product.objects.values_list('category', flat=True).distinct()
    featured_products = Product.objects.order_by('-created_at')[:5]  # Customize this query for featured products
    new_products = Product.objects.order_by('-created_at')[:5]

    return render(request, 'explore/base.html', {
        'categories': categories,
        'featured_products': featured_products,
        'new_products': new_products
    })


from django.contrib.auth import logout
from django.shortcuts import redirect





def subcategories(request, category):
    subcategories = Product.objects.filter(category=category).values_list('sub_category', flat=True).distinct()
    return render(request, 'explore/sub-categories.html', {'category': category, 'subcategories': subcategories})


def base(request):
    return render(request, 'explore/base.html', {})


def discovery(request):
    subcategory = request.GET.get('subcategory')

    if subcategory:
        products = Product.objects.filter(sub_category=subcategory)
    else:
        products = Product.objects.all()  # Show all products if no filter is applied

    # Fetch the first image for each product
    products_with_images = []
    for product in products:
        first_image = ProductImage.objects.filter(product=product).first()  # Get the first image for each product
        products_with_images.append({
            'product': product,
            'image': first_image.image.url if first_image else None  # Handle case if no image is found
        })

    return render(request, 'explore/discovery.html', {'products_with_images': products_with_images})


def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    product_images = ProductImage.objects.filter(product=product)  # Fetch all images related to this product
    return render(request, 'explore/product_detail.html', {
        'product': product,
        'product_images': product_images
    })


@login_required
def profile(request):
    # You can customize what you'd like to display on the profile page.
    return render(request, 'explore/profile.html')

'''def logout_view(request):
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page
'''