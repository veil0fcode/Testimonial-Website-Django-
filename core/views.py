from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from testimonials.models import Testimonial
from .forms import ContactForm

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_testimonials'] = Testimonial.objects.filter(approved=True)[:6]
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ContactView(CreateView):
    form_class = ContactForm
    template_name = 'core/contact.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        messages.success(self.request, "Your message has been sent successfully! We will get back to you soon.")
        return super().form_valid(form)
