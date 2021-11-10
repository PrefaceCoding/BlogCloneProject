from django.shortcuts import render, get_object_or_404, redirect
# CRUD Process in CreateView, UpdateView, and DeleteView 
from django.views.generic import (TemplateView, ListView, DetailView, 
                                    CreateView, UpdateView, DeleteView)
# not sure if explained - need to state '.' full stop means current directory in path
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils import timezone
# login_required is as it states: you need to be logged in to view url/view/function
# login_required is used for function views
from django.contrib.auth.decorators import login_required
# functions in the same way as login_reuqired, but is used for class based view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

# Create your views here.
# A simple TemplateView for the about page 
class AboutView(TemplateView):
    template_name = 'about.html'

# Using a list view will automatically look for MODELNAME_list.html - in this case post_list.html
# We can change this default behavior by creating the template_name variable
class PostListView(ListView):
    model = Post
    # The context_object_name is automatically looked for with generic views: either modelname_list or object_list
    # get_queryset adds logic to the queryset selection, allowing to specify the list of objects you want to use.
    # get_queryset over just stating queryset attribute allows for more flexible query selection
    # the usual model = Post is shorthand for the queryset
    def get_queryset(self):
        # lte = less than or equal to - SQL - we use this because we want to filter out any POST 
        # requests less than the current time (doesn't make sense to be posting from past)
        # order_by orders the list by the published date, the negative in front of the published date organizes them in descending order
        # MORE ON FILTERS: https://docs.djangoproject.com/en/3.2/topics/db/queries/#retrieving-specific-objects-with-filters
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date') 

# Similar to Listview this automatically looks for MODELNAME_detail.html
class PostDetailView(DetailView):
    model = Post
# CreateView and UpdateView don't need a success_url - it defaults to look for the get_absolute_url
class CreatePostView(LoginRequiredMixin, CreateView):
    # login_url is built in attribute expected with the loginrequiredmixin parameter
    # login_url leads you to the login page if not logged in
    login_url = '/login/'
    # redirect field name is another part of loginrequired parameter that redirects you to a certain
    # url after successfully passing arguments.
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # reverse_lazy is like using the url template tag - 
    # specifying the url name here directs you to said url
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    context_object_name = "posts"
    template_name = "post_draft_list.html"
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        # getting any posts that don't have a published date.
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


################################################################
#########################FUNCTIONS##############################
################################################################

# as stated when learning CBV - class based views are not always a replacement for functions
# while CBV does have a way of working with form (with FormView), we want to practice using functions as well.

# for functions the login_required decorator or 'paramter' is above/at the start of function
@login_required
# pk parameter links comment to post 
def add_comment_to_post(request,pk):
    # get the objects in class Post or raise 404 error instead of DOESNOTEXIST
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # remember that CommentForm is connected to the Comment class in the model
        form = CommentForm(request.POST)
        if form.is_valid():
            # commit = False means there is an object/form in memory, but the input isn't saved in the database yet
            comment = form.save(commit=False)
            # comment.post is the foreign key connection to the Post class in the model
            # = post is saying to add to the Post class/table itself 
            comment.post = post
            comment.save()
            # if function is successful, redirect loads url given in arguments
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    # the approve comment method is from the Model class Comment
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

#This is a comment remove before approval - we do not have a delete comment function/cbv
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # need to create variable to save post primary key before deleting it
    post_pk = comment.post.pk
    comment.delete()
    # The saved variable allows us to be redirected to post_detail page, otherwise a NULL value will raise error
    return redirect('post_detail', pk=post_pk)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post,pk=pk)
    model = Post
    # the publish method is from the Model class Comment and saves comment to database
    post.publish()
    return redirect('post_detail', pk=post.pk)

