from django.shortcuts import render, get_object_or_404, redirect
from products.models import Inventory, Product
from django.contrib.auth.decorators import login_required

@login_required
def inventory_list(request):
    inventories = Inventory.objects.select_related('product').all()
    return render(request, 'dashboard/inventory_list.html', {'inventories': inventories})

@login_required
def update_inventory(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        stock = int(request.POST.get('stock'))
        inventory = product.inventory
        inventory.stock = stock
        inventory.save()
        return redirect('inventory_list')
