from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    
    # To simplify the concept of Meta: think of Meta as 'settings' for the preceding class
    class Meta():
        model = Post
        #INCLUDE only these fields
        fields = ('author', 'title', 'text')
        #attrs is changing HTML class attributes
        widgets = {
            # This custom widget changes the text input field for the Forms!
            'title':forms.TextInput(attrs={'class': 'textinputclass'}),
            # This custom widget is for the medium-editor that is imported! 
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),        
        }

class CommentForm(forms.ModelForm):
    
    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author':forms.TextInput(attrs={'class': 'textinputclass'}),
            'text':forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }