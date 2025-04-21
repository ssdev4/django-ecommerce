from django.core.management.base import BaseCommand
from products.models import Product, Inventory

# run via python manage.py populate_inventory
class Command(BaseCommand):
    help = 'Create missing inventory entries for products'

    def handle(self, *args, **kwargs):
        missing_inventory = Product.objects.filter(inventory__isnull=True)
        created_count = 0

        for product in missing_inventory:
            Inventory.objects.create(product=product, stock=product.stock)
            self.stdout.write(self.style.SUCCESS(f"Created inventory for {product.name}"))
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Done! Created {created_count} inventory records."))
