import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Product, Order

def print_users():
    print("\n=== Users ===")
    users = User.objects.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

def print_products():
    print("\n=== Products ===")
    products = Product.objects.all()
    for product in products:
        print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}, Stock: {product.stock}")

def print_orders():
    print("\n=== Orders ===")
    orders = Order.objects.all()
    for order in orders:
        print(f"ID: {order.id}, User: {order.user.username}, Product: {order.product.name}, "
              f"Quantity: {order.quantity}, Status: {order.status}, Total: ${order.total_price}")

if __name__ == "__main__":
    print_users()
    print_products()
    print_orders() 