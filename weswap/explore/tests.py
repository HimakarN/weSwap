from django.test import TestCase
from .models import Product, ProductImage

class ProductDiscoveryTest(TestCase):
    def test_discovery_function(self):
        # Add setup for creating test data, like products and product images
        product = Product.objects.create(product_name="Test Product", category="Test Category", sub_category="Test Subcategory")
        ProductImage.objects.create(product=product, image='path/to/image.jpg')

        # Now call your discovery logic
        products = Product.objects.all()  # Show all products if no filter is applied

        # Fetch the first image for each product
        products_with_images = []
        for product in products:
            first_image = ProductImage.objects.filter(product=product).first()
            products_with_images.append({
                'product': product,
                'image': first_image.image.url if first_image else None
            })

        # Assertions can be added here to check the output
        self.assertEqual(len(products_with_images), 1)
        self.assertIsNotNone(products_with_images[0]['image'])
