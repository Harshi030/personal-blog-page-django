from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from .models import Author,Post,Tag
from django.views.generic import ListView
from django.views import View
from .forms import CommentForm
# Create your views here.

class home(ListView):
  template_name="blog/main_page.html"
  model=Post
  ordering=["-date"]
  context_object_name="latest_posts"
  def get_queryset(self):
    queryset= super().get_queryset()
    data=queryset[:3]
    return data
  
  

# def home(request):
#   latest_posts=Post.objects.all().order_by("-date")[:3]
#   return render(request,"blog/main_page.html",{"latest_posts":latest_posts})

class all_posts(ListView):
  template_name="blog/all_posts.html"
  model=Post
  ordering=["-date"]
  context_object_name="posts"


# def all_posts(request):
#   posts=Post.objects.all().order_by("-date")
#   return render(request,"blog/all_posts.html",{"posts":posts})


# class single_post(DetailView):
#   template_name="blog/single_post.html"
#   model=Post

#   def get_context_data(self, **kwargs):
#       context = super().get_context_data(**kwargs)
#       context["post_tags"] = self.object.tag.all()
#       context["comment_form"]=CommentForm()
#       return context
  
class single_post(View):
  def is_stored_post(self,request,post_id):
    stored_posts=request.session.get("stored_posts")
    if stored_posts is not None:
      is_saved_for_later=post_id in stored_posts
    else:
      is_saved_for_later=False
    return is_saved_for_later
  def get(self,request,slug):
    post=Post.objects.get(slug=slug)
    
    context={
      "post":post,
      "post_tags":post.tag.all(),
      "comment_form":CommentForm(),
      "comments":post.comments.all(),
      "saved_for_later":self.is_stored_post(request,post.id)
    }
    return render(request,"blog/single_post.html",context)

  def post(self,request,slug):
    comment_form=CommentForm(request.POST)
    post=Post.objects.get(slug=slug)
    if comment_form.is_valid():
      comment=comment_form.save(commit=False)
      comment.post=post
      comment.save()
      return HttpResponseRedirect(reverse("single-post",args=[slug]))
    
    context={
      "post":post,
      "post_tags":post.tag.all(),
      "comment_form":comment_form,
      "comments":post.comments.all().order_by("-id"),
      "saved_for_later":self.is_stored_post(request,post.id)
    }
    return render(request,"blog/single_post.html",context)

  

# def single_post(request,slug):
#   identified_post=Post.objects.get(slug=slug)
#   return render(request,"blog/single_post.html",{"post":identified_post,"post_tags":identified_post.tag.all()})


class ReadLaterView(View):
  def get(self,request):
    stored_posts=request.session.get("stored_posts")

    context={}
    if stored_posts is None or len(stored_posts)==0:
      context["posts"]=[]
      context["has_posts"]=False
    else:
      posts=Post.objects.filter(id__in=stored_posts)
      context["posts"]=posts
      context["has_posts"]=True
    
    return render(request,"blog/stored-posts.html",context)

  def post(self,request):
    stored_posts=request.session.get("stored_posts")
    
    if stored_posts is None:
      stored_posts=[]
    
    post_id=int(request.POST["post_id"])

    if post_id not in stored_posts:
      stored_posts.append(post_id)
     
    else:
      stored_posts.remove(post_id)
    request.session["stored_posts"]=stored_posts
    return HttpResponseRedirect("/")