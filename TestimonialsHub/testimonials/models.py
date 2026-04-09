from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='testimonials/photos/', blank=True, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    message = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='testimonials')
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_testimonials', blank=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.name} - {self.rating} Stars"

    @property
    def num_likes(self):
        return self.likes.count()
