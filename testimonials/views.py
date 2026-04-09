from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Testimonial, Category
from .forms import TestimonialForm
from django.db.models import Q

class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 9

    def get_queryset(self):
        queryset = Testimonial.objects.filter(approved=True)
        search_query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        rating = self.request.GET.get('rating')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(message__icontains=search_query))
        if category:
            queryset = queryset.filter(category__id=category)
        if rating:
            queryset = queryset.filter(rating=rating)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Pass current filters to preserve them in pagination
        context['current_q'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_rating'] = self.request.GET.get('rating', '')
        return context

class TestimonialCreateView(LoginRequiredMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'testimonials/testimonial_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TestimonialUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'testimonials/testimonial_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        testimonial = self.get_object()
        return self.request.user == testimonial.user

class TestimonialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Testimonial
    template_name = 'testimonials/testimonial_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        testimonial = self.get_object()
        return self.request.user == testimonial.user

class LikeTestimonialView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        testimonial_id = request.POST.get('testimonial_id')
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)

        if testimonial.likes.filter(id=request.user.id).exists():
            testimonial.likes.remove(request.user)
            liked = False
        else:
            testimonial.likes.add(request.user)
            liked = True

        return JsonResponse({
            'liked': liked,
            'num_likes': testimonial.likes.count()
        })
