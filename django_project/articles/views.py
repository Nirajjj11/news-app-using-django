from django.shortcuts import render
# List and detail generic views for article display
from django.views.generic import ListView, DetailView
# Edit views: Create, Update, Delete for article management
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy, reverse
from .models import Article 
from .forms import CommentForm
# Generic View for handling both GET and POST requests
from django.views import View

# CRITICAL: Authorization mixins to enforce user permissions
# LoginRequiredMixin - redirects unauthenticated users to login
# UserPassesTestMixin - allows fine-grained permission control via test_func()
from django.contrib.auth.mixins import (
      LoginRequiredMixin,
      UserPassesTestMixin,
)


class ArticleListView(ListView): 
      # CRITICAL: Displays all articles publicly (no login required)
      model = Article 
      template_name = "article_list.html"

class ArticleDetailView(LoginRequiredMixin, DetailView):
      # IMPORTANT: Requires login to view article details
      model = Article
      template_name = 'article_detail.html'
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # CRITICAL: Inject comment form for template rendering
            context['form'] = CommentForm() 
            return context

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
      # CRITICAL: Enforces authentication + author-only permission
      model = Article
      fields = (
            'title',
            'body',
      )
      template_name = "article_edit.html"
      
      def test_func(self):
            # CRITICAL: Verify current user is the article author
            obj = self.get_object()
            return obj.author == self.request.user
      
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
      # CRITICAL: Enforces authentication + author-only permission
      model = Article
      template_name = "article_delete.html"
      success_url = reverse_lazy("article_list")
      
      def test_func(self):
            # CRITICAL: Verify current user is the article author
            obj = self.get_object()
            return obj.author == self.request.user
      
class ArticleCreateView(LoginRequiredMixin, CreateView):
      # CRITICAL: Only authenticated users can create articles
      model = Article
      template_name = "article_new.html"
      fields = (
            "title",
            "body",
      )
      
      def form_valid(self, form):
            # CRITICAL: Auto-assign current user as article author
            form.instance.author = self.request.user
            return super().form_valid(form)
      
class CommentGet(DetailView):
      # IMPORTANT: Handles GET request to display article with comment form
      model = Article
      template_name = "article_detail.html"
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # CRITICAL: Inject empty comment form for user input
            context['form'] = CommentForm()
            return context
      
class CommentPost():  
      # PLACEHOLDER: Will be replaced with proper FormView below
      pass 


class ArticleDetailView(LoginRequiredMixin, View):
      # CRITICAL: Hybrid view routing GET and POST to appropriate handlers
      def get(self, request, *args, **kwargs): 
            # Route GET requests through CommentGet handler
            view = CommentGet.as_view() 
            return view(request, *args, **kwargs) 
      
      def post(self, request, *args, **kwargs):
            # Route POST requests through CommentPost handler   
            view = CommentPost.as_view() 
            return view(request, *args, **kwargs) 

class CommentPost(SingleObjectMixin, FormView):
      # CRITICAL: Handles POST request to create new comment
      model = Article 
      form_class = CommentForm 
      template_name = "article_detail.html" 
      
      def post(self, request, *args, **kwargs): 
            # IMPORTANT: Retrieve article object first for context
            self.object = self.get_object() 
            return super().post(request, *args, **kwargs) 
      
      def form_valid(self, form):
            # CRITICAL SECTION: Process comment creation with proper associations
            comment = form.save(commit=False) 
            comment.article = self.object  # IMPORTANT: Link comment to article
            comment.author = self.request.user  # CRITICAL: Auto-assign current user as comment author
            comment.save() 
            return super().form_valid(form) 
      
      def get_success_url(self): 
            article = self.object 
            return reverse("article_detail", kwargs={"pk": article.pk})   