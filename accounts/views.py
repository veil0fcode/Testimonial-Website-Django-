from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from testimonials.models import Testimonial

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dashboard')

class DashboardView(LoginRequiredMixin, ListView):
    model = Testimonial
    template_name = 'accounts/dashboard.html'
    context_object_name = 'testimonials'

    def get_queryset(self):
        return Testimonial.objects.filter(user=self.request.user)
