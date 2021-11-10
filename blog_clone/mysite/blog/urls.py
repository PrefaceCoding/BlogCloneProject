from django.urls import path
from . import views

#all pattern and no play make Jack a dull boy.
urlpatterns= [
    # Using a list view will automatically look for modelname_list.html - in this case post_list.html
    path('', views.PostListView.as_view(), name='post_list'),
    # About html is specified in views
    path('about/', views.AboutView.as_view(), name = 'about'),
    # Similar to list view this will default to looking for template modelname_detail.html - post_detail.html
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # defaults to look for modelname_form.html - post_form.html
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    # defaults to look for modelname_form.html - post_form.html (We are editing from same page as create form)
    path('post/<str:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    # defaults to look for modelname_confirm_delete.html - post_confirm_delete.html
    path('post/<str:pk>/remove/', views.PostDeleteView.as_view(), name='post_delete'),
    path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    # The urls for comment is specified in view function.
    path('post/<str:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    # calling primary key to approve for the functions
    path('comment/<str:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<str:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
]

