from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('add/', views.TestimonialCreateView.as_view(), name='testimonial_create'),
    path('<int:pk>/edit/', views.TestimonialUpdateView.as_view(), name='testimonial_update'),
    path('<int:pk>/delete/', views.TestimonialDeleteView.as_view(), name='testimonial_delete'),
    path('like/', views.LikeTestimonialView.as_view(), name='testimonial_like'),
]
