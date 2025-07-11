from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import ClothingStyle
import json

@csrf_exempt
@require_http_methods(["GET"])
def clothing_styles_api(request):
    """REST API endpoint for clothing styles (optional)"""
    try:
        styles = ClothingStyle.objects.filter(is_active=True)
        data = []
        for style in styles:
            data.append({
                'id': str(style.id),
                'name': style.name,
                'description': style.description,
                'cost': float(style.cost),
                'image': style.image,
                'isActive': style.is_active,
            })
        return JsonResponse({'clothing_styles': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)