from django import forms

from .models import Post, Comments

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        exclude = ('author', 'is_published')
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': ''})
        } 


class CommentsForm(forms.ModelForm):

        class Meta:
            model = Comments
            fields = ('text',)