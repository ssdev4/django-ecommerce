from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Inventory for {self.product.name}"

    def update_stock(self, quantity):
        """Helper function to update stock when an order is placed."""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
        else:
            raise ValueError("Not enough stock available.")
