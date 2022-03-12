from attr import field
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import BlogPost
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.

class BlogPostCreateView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'c_admin/blogcreate.html'
    fields = ['title', 'body', 'tags']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)