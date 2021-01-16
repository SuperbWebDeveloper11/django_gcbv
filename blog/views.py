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
from .models import Post, Comment
from .forms import CommentForm


class PostList(ListView): 
    model = Post
    template_name = 'blog/post/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5


class PostCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView): # create post 
    model = Post
    initial = {'title': 'new post'}
    template_name = 'blog/post/post_form_create.html' 
    fields = ['title']
    success_message = "post was created successfully"

    def form_valid(self, form):
        form.instance.created_by = self.request.user 
        return super().form_valid(form)


class PostUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView): # update post 
    model = Post
    template_name = 'blog/post/post_form_update.html' 
    fields = ['title']
    success_message = "post was updated successfully"

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")

# delete post 
class PostDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post/post_confirm_delete.html' 
    success_message = "post was deleted successfully"
    success_url = reverse_lazy('post:post_list')

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


# ************* create comment ************* 
class PostDetail(SingleObjectMixin, View): 
    model = Post

    # display detail page with post instance and comment_form
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForm()
        context = {'post': post, 'comment_form': comment_form}
        return render(request, 'blog/post/post_detail.html', context)

    # save comment form and redisplay detail page with post instance and comment_form
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        post = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.created_by = request.user
            comment_form.instance.post = post
            comment_form.save()
        context = {'post': post, 'comment_form': comment_form}
        return render(request, 'blog/post/post_detail.html', context)


# ************* update comment ************* 
class PostUpdateComment(SingleObjectMixin, View): 
    model = Post

    # display detail page with post instance and comment_form
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        current_comment = get_object_or_404(Comment, post=post, pk=kwargs['comment_pk'])
        comment_form = CommentForm(instance=current_comment)
        context = {'post': post, 'comment_form': comment_form, 'update_form': True}
        return render(request, 'blog/post/post_detail.html', context)

    # update comment and redisplay detail page with post instance and comment_form
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        post = self.get_object()
        current_comment = get_object_or_404(Comment, post=post, pk=kwargs['comment_pk'])
        comment_form = CommentForm(request.POST, instance=current_comment)
        if comment_form.is_valid():
            # update comment manually
            new_content = comment_form.cleaned_data['content']
            current_comment.content = new_content 
            current_comment.save()
        context = {'post': post, 'comment_form': comment_form}
        return render(request, 'blog/post/post_detail.html', context)


# ************* delete comment ************* 
class PostDeleteComment(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post/comment_confirm_delete.html' 
    success_message = "comment was deleted successfully"

    def get_success_url(self):
        # redirect to post detail
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def get_object(self):
        post = super().get_object()
        current_comment = get_object_or_404(Comment, post=post, pk=self.kwargs['comment_pk'])
        return current_comment

    def form_valid(self, form):
        if form.instance.created_by == self.request.user:
            return super().form_valid(form)
        else:
            return HttpResponse("you don't have permissions")


