from django.db import models
# If we look into settings and see the TIME_ZONE variable, we notice that it is in UTC (Coordinated Universal Time)
# We can change this to match the local time but it is recommended by Django to use UTC - at least in a development environment.
from django.utils import timezone
from django.urls import reverse
# User model is a very important concept that will be explained in slides, but the gist is that it comes with its own attributes built-in by Django
# We have already seen the User being created when using createsuperuser and can see the fields from admin.
# The primary attributes are: username, password, email, first_name, and last_name, but it includes much more: 
# https://docs.djangoproject.com/en/3.2/ref/contrib/auth/#django.contrib.auth.models.User
from django.contrib.auth.models import User

class Post(models.Model):
    # User is called for here, and includes prebuilt attributes as stated before.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    # timezone.now calls for the current time for UTC
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    # publish method -> published_date -> save to database
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # using the comments related_name, we filter out only the approved comments.
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
    
    # get_absolute_url (e.g in this case post/<pk>)
    def get_absolute_url(self):
        return reverse('post_detail', kwargs= {'pk': self.pk})
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    # We are calling for related_name for ease of use later on - much like assigning names in URL
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    # We want approved_comment (or any new comment) to have some way of returning a 'False' value so they
    # aren't immediately approved/published and be put in database
    approved_comment = models.BooleanField(default=False)
    
    # By default the comments have the Boolean value of 0 or False, but this method changes it to True or 1
    # allowing comments to be published
    def approve(self):
        self.approved_comment = True
        self.save()

    # This method is for determining what url to go to when creating a comment
    def get_absolute_url(self):
        return reverse('post_list')
    
    def __str__(self):
        return self.text
