from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from PIL import Image
import os

def user_photo_path(instance, filename):
    # Get file extension
    ext = filename.split('.')[-1]
    # Create filename with user's username
    filename = f"{instance.username}_photo.{ext}"
    # Return the path
    return os.path.join('user_photos', filename)

class User(AbstractUser):
    photo = models.ImageField(
        upload_to=user_photo_path,
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])
        ],
        help_text="Upload a profile photo (max 2MB, supported formats: JPG, JPEG, PNG, WebP)"
    )

    # Fix related name conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.photo:
            # Open the image
            img = Image.open(self.photo.path)
            
            # Get the current dimensions
            width, height = img.size
            
            # Calculate the size for a square crop
            size = min(width, height)
            
            # Calculate the coordinates for the crop
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            
            # Crop the image
            img = img.crop((left, top, right, bottom))
            
            # Save the cropped image
            img.save(self.photo.path)

    def clean(self):
        super().clean()
        if self.photo and self.photo.size > 2 * 1024 * 1024:  # 2MB in bytes
            raise ValidationError('Photo size must be no more than 2MB.')

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField('User', blank=True, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title 