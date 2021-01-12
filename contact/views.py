from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import ContactForm


# render 'contact/contact.html' for the user
class Contact(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contact:success')

    def form_valid(self, form):
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        print(' title: {}, \n message: {}'.format(title, message))
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid contact form')
        return super().form_invalid(form)


# render 'contact/contact_success.html' for the user
class ContactSuccess(TemplateView):
    template_name = 'contact/contact_success.html'
    
