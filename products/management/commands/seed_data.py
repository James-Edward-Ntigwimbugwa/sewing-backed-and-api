# products/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from products.models import ClothingStyle
import uuid

class Command(BaseCommand):
    help = 'Seed the database with sample clothing styles'

    def handle(self, *args, **options):
        # Clear existing data
        ClothingStyle.objects.all().delete()
        
        sample_styles = [
            {
                'name': 'Casual T-Shirt',
                'description': 'Comfortable cotton t-shirt perfect for everyday wear. Available in multiple colors.',
                'cost': 25000.00,
                'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300&h=300&fit=crop',
            },
            {
                'name': 'Elegant Dress',
                'description': 'Beautiful evening dress with intricate embroidery and flowing fabric.',
                'cost': 85000.00,
                'image': 'https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=300&h=300&fit=crop',
            },
            {
                'name': 'Business Suit',
                'description': 'Professional tailored suit perfect for office meetings and formal events.',
                'cost': 150000.00,
                'image': 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=300&h=300&fit=crop',
            },
            {
                'name': 'Denim Jeans',
                'description': 'Classic blue jeans with comfortable fit and durable fabric.',
                'cost': 45000.00,
                'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=300&h=300&fit=crop',
            },
            {
                'name': 'Summer Blouse',
                'description': 'Light and airy blouse perfect for hot summer days.',
                'cost': 35000.00,
                'image': 'https://images.unsplash.com/photo-1564257577-0f76d7166e22?w=300&h=300&fit=crop',
            },
            {
                'name': 'Winter Coat',
                'description': 'Warm and stylish coat to keep you comfortable during cold weather.',
                'cost': 120000.00,
                'image': 'https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=300&h=300&fit=crop',
            },
            {
                'name': 'Sports Hoodie',
                'description': 'Comfortable hoodie perfect for workouts and casual activities.',
                'cost': 55000.00,
                'image': 'https://images.unsplash.com/photo-1556821840-3a9fac6de5f1?w=300&h=300&fit=crop',
            },
            {
                'name': 'Formal Shirt',
                'description': 'Crisp white shirt ideal for business meetings and formal occasions.',
                'cost': 40000.00,
                'image': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=300&h=300&fit=crop',
            },
            {
                'name': 'Maxi Dress',
                'description': 'Flowing maxi dress with beautiful prints, perfect for special occasions.',
                'cost': 75000.00,
                'image': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=300&h=300&fit=crop',
            },
            {
                'name': 'Leather Jacket',
                'description': 'Stylish leather jacket that adds edge to any outfit.',
                'cost': 180000.00,
                'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=300&h=300&fit=crop',
            },
            {
                'name': 'Polo Shirt',
                'description': 'Classic polo shirt perfect for smart casual occasions.',
                'cost': 30000.00,
                'image': 'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=300&h=300&fit=crop',
            },
            {
                'name': 'Cocktail Dress',
                'description': 'Elegant cocktail dress perfect for evening parties and events.',
                'cost': 95000.00,
                'image': 'https://images.unsplash.com/photo-1566479179817-c0b38a2b68e7?w=300&h=300&fit=crop',
            },
        ]

        for style_data in sample_styles:
            style = ClothingStyle.objects.create(**style_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created clothing style: {style.name}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded {len(sample_styles)} clothing styles')
        )

