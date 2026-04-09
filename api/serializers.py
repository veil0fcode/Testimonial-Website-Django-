from rest_framework import serializers
from django.contrib.auth.models import User
from testimonials.models import Testimonial, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TestimonialSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Testimonial
        fields = ['id', 'user', 'user_name', 'name', 'photo', 'rating', 'message', 'category', 'category_name', 'created_date', 'approved', 'num_likes']
        read_only_fields = ['user', 'approved']
