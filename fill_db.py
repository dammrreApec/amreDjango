import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amrestore.settings')
django.setup()

from store.models import Product, Category

def populate():
    
    print("Cleaning database...")
    Product.objects.all().delete()

   
    shoes, _ = Category.objects.get_or_create(name="Shoes")
    bags, _ = Category.objects.get_or_create(name="Accessories")
    clothes, _ = Category.objects.get_or_create(name="Clothing")

    
    items = [
        {
            "name": "Classic Leather Shoes",
            "price": 35750, "cat": shoes,
            "desc": "Elegant leather shoes perfect for formal occasions and everyday wear.",
            "img": "1.png"
        },
        {
            "name": "Designer Handbag",
            "price": 23100, "cat": bags,
            "desc": "Stylish designer handbag with premium materials and spacious compartments.",
            "img": "2.png"
        },
        {
            "name": "Athletic Running Shoes",
            "price": 20900, "cat": shoes,
            "desc": "High-performance running shoes with advanced cushioning and support.",
            "img": "3.png"
        },
        {
            "name": "Travel Backpack",
            "price": 15950, "cat": bags,
            "desc": "Durable travel backpack with multiple compartments and ergonomic design.",
            "img": "4.png"
        },
        {
            "name": "Cotton Graphic T-Shirt",
            "price": 9900, "cat": clothes,
            "desc": "Comfortable cotton t-shirt with trendy graphic design and soft fabric.",
            "img": "5.png"
        },
        {
            "name": "Stylish Polo Shirt",
            "price": 12100, "cat": clothes,
            "desc": "Classic polo shirt with modern fit and premium cotton blend material.",
            "img": "6.png"
        }
    ]

    
    for item in items:
        Product.objects.create(
            name=item['name'],
            price=item['price'],
            category=item['cat'],
            description=item['desc'],
            image=item['img']
        )
    
    print("Success: Fashion products with images added!")


if __name__ == '__main__':
    populate()