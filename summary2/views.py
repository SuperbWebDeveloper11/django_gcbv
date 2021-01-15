from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
# messages framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
# class-based generic views
from django.views.generic import TemplateView, ListView, DetailView, View, FormView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import SingleObjectMixin
# import models
from django.contrib.auth.models import User
from .models import Summary
from .forms import CommentForm


class SummaryList(ListView): 
    model = Summary
    template_name = 'summary2/summary/summary_list.html'
    context_object_name = 'summary_list'
    paginate_by = 5


# ******************** app 1 ******************** 
class SummaryDetail(SingleObjectMixin, View): 
    model = Summary

    # display detail page with summary instance and comment_form
    def get(self, request, *args, **kwargs):
        summary = self.get_object()
        comment_form = CommentForm()
        context = {'summary': summary, 'comment_form': comment_form}
        return render(request, 'summary2/summary/summary_detail.html', context)

    # save comment form and redisplay detail page with summary instance and comment_form
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        summary = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.created_by = request.user
            comment_form.instance.summary = summary
            comment_form.save()
        context = {'summary': summary, 'comment_form': comment_form}
        return render(request, 'summary2/summary/summary_detail.html', context)


# ******************** app 2 ******************** 
class SummaryDetail2(SingleObjectMixin, ListView): 
    paginate_by = 2
    template_name = 'summary2/summary/summary_detail2.html'

    def get(self, request, *args, **kwargs):
        # return summary instance
        # we pass queryset explicitly, otherwise it will use get_queryset() method
        self.object = self.get_object(queryset=Summary.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add summary instance on context
        context['summary'] = self.object
        return context

    def get_queryset(self):
        # return summary comments
        return self.object.comments.all()


# ******************** app 3 ******************** 
class SummaryDisplay(SingleObjectMixin, View): 
    model = Summary

    # display detail page with summary instance and comment_form
    def get(self, request, *args, **kwargs):
        summary = self.get_object()
        comment_form = CommentForm()
        context = {'summary': summary, 'comment_form': comment_form}
        return render(request, 'summary2/summary/summary_detail3.html', context)

class SummaryComment(SingleObjectMixin, FormView):
    model = Summary

    # save comment form and redisplay detail page with summary instance and comment_form
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        summary = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.created_by = request.user
            comment_form.instance.summary = summary
            comment_form.save()
        context = {'summary': summary, 'comment_form': comment_form}
        return render(request, 'summary2/summary/summary_detail3.html', context)

class SummaryDetail3(View):
    
    def get(self, request, *args, **kwargs):
        view = SummaryDisplay.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = SummaryComment.as_view()
        return view(request, *args, **kwargs)


class SummaryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create summary 
    model = Summary
    initial = {'title': 'new summary'}
    template_name = 'summary2/summary/summary_form_create.html' 
    fields = ['title']
    success_message = "summary was created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user 
        return super().form_valid(form)


class SummaryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update summary 
    model = Summary
    template_name = 'summary2/summary/summary_form_update.html' 
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
    template_name = 'summary2/summary/summary_confirm_delete.html' 
    success_message = "summary was deleted successfully"
    success_url = reverse_lazy('summary:summary_list')

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


