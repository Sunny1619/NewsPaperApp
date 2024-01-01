
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, FormView
from django.urls import reverse_lazy, reverse
from .models import Articles
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from .forms import CommentForm

class ArticleListView(LoginRequiredMixin, ListView):
    model = Articles
    template_name = 'article_list.html'

class CommentGet(DetailView):
    model = Articles
    template_name = 'article_detail.html'

    extra_context={'form':CommentForm}

class CommentPost(SingleObjectMixin, FormView):
    model = Articles
    form_class = CommentForm
    template_name = 'article_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        article= self.get_object()
        return reverse('article_detail', kwargs={'pk':article.pk})
    
class ArticleDetailView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)

class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articles
    template_name = 'article_edit.html'
    fields = [
        'title',
        'body',
    ]
    def test_func(self):
        obj=self.get_object()
        return obj.author==self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articles
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
    def test_func(self):
        obj=self.get_object()
        return obj.author==self.request.user

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Articles
    template_name = 'article_create.html'
    fields = [
        'title',
        'body',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


