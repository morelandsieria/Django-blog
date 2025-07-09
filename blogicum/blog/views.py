from datetime import datetime

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PostForm, CommentsForm
from .models import Category, Post, Comments


User = get_user_model()


class PostListView(ListView):
    model = Post
    ordering = 'id'
    paginate_by = 10
    template_name = 'blog/index.html'
    def get_queryset(self):
        return Post.objects.select_related('location', 'category').filter(
            is_published=True,
            location__is_published=True,
            pub_date__lt=datetime.now(),
            category__is_published=True,
            category__created_at__lt=datetime.now(),
            )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm()
        context['comments'] = (
            self.object.comments.select_related('author')
            )
        return context


class CategoryListView(ListView):
    model = Post
    ordering = 'id'
    paginate_by = 10
    template_name = 'blog/category.html'

    def get_queryset(self):
        return Post.objects.select_related('location', 'category').filter(
            is_published=True,
            pub_date__lt=datetime.now(),
            category__is_published=True,
            category__created_at__lt=datetime.now(),
            category__slug=self.kwargs['category_slug']
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index') 


class UserDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index') 


class CommentCreateView(LoginRequiredMixin, CreateView):
    comment = None
    model = Comments
    form_class = CommentsForm
    # template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.comment = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.comment.pk})


class CommentUpdateView(UpdateView):
    model = Comments
    form_class = CommentsForm
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('blog:index') 


class commentDeleteView(DeleteView):
    model = Comments
    success_url = reverse_lazy('blog:index') 