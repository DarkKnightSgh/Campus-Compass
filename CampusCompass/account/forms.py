from django import forms
from .models import ClubMember

class ClubMembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = ClubMember
        fields = ['user', 'social_media_manager','club_head']
        widgets = {

        }