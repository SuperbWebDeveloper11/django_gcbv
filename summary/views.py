from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
# messages framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# class-based generic views
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
# import models
from django.contrib.auth.models import User
from .models import Summary


class SummaryList(ListView): 
    model = Summary
    template_name = 'summary/summary/summary_list.html'
    context_object_name = 'summary_list'
    paginate_by = 5


class SummaryDetail(DetailView): 
    model = Summary
    template_name = 'summary/summary/summary_detail.html'
    context_object_name = 'summary'


class SummaryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create summary 
    model = Summary
    initial = {'title': 'another summary'}
    template_name = 'summary/summary/summary_form_create.html' 
    fields = ['title']
    success_message = "summary was created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user 
        return super().form_valid(form)


class SummaryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update summary 
    model = Summary
    template_name = 'summary/summary/summary_form_update.html' 
    fields = ['title']
    success_message = "summary was updated successfully"

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")

# delete summary 
class SummaryDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Summary
    template_name = 'summary/summary/summary_confirm_delete.html' 
    success_message = "summary was deleted successfully"
    success_url = reverse_lazy('summary:summary_list')

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


