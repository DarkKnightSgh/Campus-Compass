from django import forms
from .models import Resource
from branch.models import Branch


class ResourceForm(forms.ModelForm):
    branch = forms.ModelMultipleChoiceField(
        queryset=Branch.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    class Meta:
        model = Resource
        fields = (
        'title',
        'files',
        'tags',
        'branch',
        )