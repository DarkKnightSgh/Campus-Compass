from .models import Announcement
from django import forms
from django.forms import CheckboxSelectMultiple

from branch.models import Branch
import markdown


class AnnouncementForm(forms.ModelForm):
    branch = forms.ModelMultipleChoiceField(
        queryset=Branch.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes for multiple selections
        required=True  
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Announcement
        fields = (
        'title',
        'content',
        'featured_img',
        'branch',
        )
        