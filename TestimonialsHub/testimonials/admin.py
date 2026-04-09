from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Testimonial

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.action(description='Approve selected testimonials')
def approve_testimonials(modeladmin, request, queryset):
    queryset.update(approved=True)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'rating', 'approved', 'created_date', 'category')
    list_filter = ('approved', 'rating', 'category', 'created_date')
    search_fields = ('name', 'message')
    actions = [approve_testimonials]
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.photo.url)
        return "No Image"
    photo_preview.short_description = "Photo Preview"
