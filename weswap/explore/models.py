# explore/models.py

from django.db import models
from django.utils import timezone


# Product model
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)  # Automatically assigns a unique product_id starting from 1
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    description = models.TextField()
    product_condition = models.CharField(max_length=50)
    product_age = models.IntegerField(help_text='Product age in months or years')
    product_price = models.IntegerField(help_text='Base price of product')
    product_size = models.CharField(max_length=50)
    product_color = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name


# ProductImage model for storing multiple images for each product
class ProductImage(models.Model):
    product = models.ForeignKey(Product, to_field='product_id', on_delete=models.CASCADE)  # Foreign key to Product
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Path to store product images

    def __str__(self):
        return f"Image for {self.product.product_name}"
