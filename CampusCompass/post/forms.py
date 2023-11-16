from .models import Post
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.forms import CheckboxSelectMultiple

from branch.models import Branch
import markdown


class PostForm(forms.ModelForm):
    content= forms.CharField(widget=CKEditorWidget(config_name='default'))

    branch = forms.ModelMultipleChoiceField(
        queryset=Branch.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for multiple selections
        required=True  
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = (
        'title',
        'content',
        'tags',
        'branch',
        )
        