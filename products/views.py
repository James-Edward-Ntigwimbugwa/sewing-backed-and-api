# products/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import ClothingStyle

def clothing_styles_api(request):
    """REST API endpoint for clothing styles (optional)"""
    styles = ClothingStyle.objects.filter(is_active=True)
    data = []
    for style in styles:
        data.append({
            'id': str(style.id),
            'name': style.name,
            'description': style.description,
            'cost': float(style.cost),
            'image': style.image,
        })
    return JsonResponse({'clothing_styles': data})