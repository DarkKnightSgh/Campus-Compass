from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect

from .models import Announcement

from django.contrib import messages

# get forms
from .forms import AnnouncementForm

# import login required
from django.contrib.auth.decorators import login_required
from account.decorator import club_head_required

# Create your views here.

@login_required(login_url='/account/login')
@club_head_required 
def create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            # save
            announcement = form.save(commit=False)
            announcement.post_by = request.user
            announcement.save()
            form.save_m2m() # for saving many to many
            return redirect('/announcement')
        else:
            return render(request, 'announcement/create_announcement.html', {'form': form})
    else:
        form = AnnouncementForm()
        return render(request, 'announcement/create_announcement.html', {'form': form})