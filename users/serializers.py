from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Order, Post
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'photo']
        read_only_fields = ['id']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'photo']

    def validate_photo(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:  # 2MB in bytes
                raise ValidationError('Photo size must be no more than 2MB.')
            if not value.content_type.startswith('image/'):
                raise ValidationError('File must be an image.')
        return value

    def validate(self, data):
        if not data.get('username'):
            raise ValidationError({'username': 'Username is required.'})
        if not data.get('email'):
            raise ValidationError({'email': 'Email is required.'})
        if not data.get('password'):
            raise ValidationError({'password': 'Password is required.'})
        return data

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                photo=validated_data.get('photo')
            )
            return user
        except Exception as e:
            raise ValidationError(str(e))

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'total_price', 'created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'created_at', 'updated_at', 'likes_count', 'is_liked')
        read_only_fields = ('author', 'created_at', 'updated_at')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False 