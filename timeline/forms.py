from django import forms
from .models import post
from .models import comment


class Add_post(forms.ModelForm):

    class Meta:
        model = post
        fields = ["title", "rating", "review", "image"]


class Add_Comment(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['comment']

class edit_post(forms.ModelForm):

    class Meta:
        model = post
        # fields = "__all__"
        fields = ["title", "author", "rating", "review", "image"]

class delete_post(forms.ModelForm):
     class Meta:
        model = post
        fields=[]


class edit_comment(forms.ModelForm):
    class Meta:
        model = comment      
        fields = ["comment"]

class delete_comment(forms.ModelForm):
     class Meta:
        model = comment
        fields=[]
