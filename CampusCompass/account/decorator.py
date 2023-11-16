from .models import User, Club,ClubMember
from django.shortcuts import redirect
from django.contrib import messages

# create a decorator to check if the user is club head or social media manager or not

def is_club_head(username):
    try:
        user=User.objects.get(username=username)
        club_member=ClubMember.objects.get(user=user)
        if club_member.club_head:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    

def is_social_media_manager(username):
    try:
        user=User.objects.get(username=username)
        club_member=ClubMember.objects.get(user=user)
        if club_member.social_media_manager:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    
def which_club_head(username):
    try:
        user=User.objects.get(username=username)
        club_member=ClubMember.objects.get(user=user)
        if club_member.club_head:
            return club_member.club
        else:
            return False
    except Exception as e:
        print(e)
        return False

def which_club_social_media_manager(username):
    try:
        user=User.objects.get(username=username)
        club_member=ClubMember.objects.get(user=user)
        if club_member.social_media_manager:
            return club_member.club
        else:
            return False
    except Exception as e:
        print(e)
        return False

# create decorator

def club_head_required(view_func):
    def wrapper_func(request,*args,**kwargs):
        if is_club_head(request.user.__str__()):
            return view_func(request,*args,**kwargs)
        else:
            # message
            messages.info(request,"You are not authorized to access this page")
            return redirect('/error404')
    return wrapper_func   

def social_media_manager_required(view_func):
    def wrapper_func(request,*args,**kwargs):
        if is_social_media_manager(request.user.__str__()):
            return view_func(request,*args,**kwargs)
        else:
            # message
            messages.info(request,"You are not authorized to access this page")
            return redirect('/error404')
    return wrapper_func

def club_head_or_social_media_manager_required(view_func):
    def wrapper_func(request,*args,**kwargs):
        if is_club_head(request.user.__str__()) or is_social_media_manager(request.user.__str__()):
            return view_func(request,*args,**kwargs)
        else:
            # message
            messages.error(request,"You are not authorized to access this page!! Only Club heads and social media managers allowed")
            return redirect('/error404')
    return wrapper_func

def is_club_member(username):
    try:
        user=User.objects.get(username=username)
        club_member=ClubMember.objects.get(user=user)
        return True
    except Exception as e:
        print(e)
        return False

def which_club_member(username):
    try:
        user=User.objects.get(username=username)
        club_member=ClubMember.objects.get(user=user)
        return club_member.club
    except Exception as e:
        print(e)
        return False


