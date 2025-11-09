from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializer
import json

# ---------- Validation Functions ----------
def validate_file(file):
    max_size = 5 * 1024 * 1024
    if file.size > max_size:
        return False, 'file size is exceeded'
    allowed_type = ['image/png', 'image/jpeg', 'application/pdf']
    if file.content_type not in allowed_type:
        return False, 'file with jpg, png, pdf extensions only allowed'
    return True, 'valid'


def validate_price(price):
    if len(price) > 0 and price.isdigit():
        return True, 'validated'
    return False, 'update price value greater than 0 and must be a digit'


# ---------- Main API View ----------
@csrf_exempt
def product_details(req):
    # ----- POST (Create Product) -----
    if req.method == 'POST':
        data = {
            'name': req.POST.get('name'),
            'description': req.POST.get('description'),
            'price': req.POST.get('price'),
        }
        photo = req.FILES.get('photo')
        data['photo'] = photo

        final_data = ProductSerializer(data=data)
        if final_data.is_valid():
            final_data.save()
            return JsonResponse({'products_details': final_data.data})
        else:
            return JsonResponse(final_data.errors)

    # ----- GET (Fetch All Products) -----
    elif req.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'Details': serializer.data}, safe=False)

    # ----- PATCH (Update Product) -----
    elif req.method == "PATCH":
        body = json.loads(req.body)
        product_id = body.get("id")

        if not product_id:
            return JsonResponse({"error": "Product ID is required for PATCH"})

        products = Product.objects.filter(id=product_id)
        if not products.exists():
            return JsonResponse({"error": "Product not found"})

        product = products.first()
        serializer = ProductSerializer(product, data=body, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"patched data": serializer.data})
        else:
            return JsonResponse(serializer.errors)

    # ----- DELETE (Delete Product) -----
    elif req.method == "DELETE":
        body = json.loads(req.body)
        product_id = body.get("id")

        if not product_id:
            return JsonResponse({"error": "Product ID is required for DELETE"})

        product = Product.objects.filter(id=product_id).first()
        if not product:
            return JsonResponse({"error": "Product not found"})

        product.delete()
        return JsonResponse({"message": f"Product with ID {product_id} deleted successfully"})

    # ----- METHOD NOT ALLOWED -----
    else:
        return JsonResponse({"error": "Method not allowed"})
