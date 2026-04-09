from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from testimonials.models import Testimonial, Category
from .serializers import UserSerializer, CategorySerializer, TestimonialSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class TestimonialViewSet(viewsets.ModelViewSet):
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Only return approved testimonials for unauthorized users, or all for admins
        if self.request.user.is_staff:
            return Testimonial.objects.all()
        return Testimonial.objects.filter(approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
