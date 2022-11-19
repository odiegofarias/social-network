from django import forms
from .models import Post, Comment


class PostModelForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={'rows': 2}
        ))
    class Meta:
        model = Post
        fields = ('content', 'image')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={'placeholder': 'Adicionar comentário'}
        )
    )
    class Meta:
        model = Comment
        fields = ('body', )