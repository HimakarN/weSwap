
# explore/models.py

from django.db import models
#from user_authorization.models import User  # Import the User model

class Product(models.Model):
    #user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User model
    product_id = models.IntegerField(unique="True")
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # For storing product images
    product_condition = models.CharField(max_length=50)  # e.g., 'New', 'Used'
    product_age = models.IntegerField(help_text='Product age in months or years')
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.product_name
