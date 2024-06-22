from django.urls import path
from . import views

urlpatterns = [
    path("",views.home.as_view(),name="home-page"),
    path("posts",views.all_posts.as_view(),name="all-posts"),
    path("post/<slug:slug>",views.single_post.as_view(),name="single-post"),
    path("read-later",views.ReadLaterView.as_view(),name="read-later")
]
