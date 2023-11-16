from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import *
from django.contrib import messages
import re
from taggit.models import Tag

from django.http import JsonResponse
from django.db.models import Subquery, OuterRef, Avg, Count

# Create your views here.

def create_slug(username,title):
    # remove all special character except space
    slug = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    # replace all space with -
    slug= username+" "+slug
    slug = slug.lower()
    slug = re.sub(r'\s', '-', slug)
    return slug


@login_required(login_url='/account/login')
def edit_post(request,slug):
    username=request.user.__str__()
    post=Post.objects.get(slug=slug)
    user=User.objects.get(username=username)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid() and post.user==user:
            # get branches
            branches = form.cleaned_data['branch']
            # get tags
            tags = form.cleaned_data['tags']
            # get title
            title = form.cleaned_data['title']

            # create slug
            slug = create_slug(username,title)

            post = form.save(commit=False)
            # post.user = User.objects.get(username=username)
            post.author = post.user.first_name+" "+post.user.last_name
            post.slug = slug
            post.save()
            # add branches
            for branch in branches:
                post.branch.add(branch)
            # add tags
            for tag in tags:
                tag = tag.strip().lower()
                domain, created = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag)
            messages.success(request, "Post successfully created!")
            return redirect("/post/feed")
        else:
            messages.error(request, "Error in form submission. Please correct the errors below.")

    # store default post value in form
    form = PostForm(instance=post)
    context={
        'form':form
    }
    return render(request,'post/edit_post.html',context)


@login_required(login_url='/account/login')
def feed(request):
    username=request.user.__str__()
    # print(request.user.student.branch)
    user_branch = request.user.student.branch 
    # Filter posts by the user's branch
    post = Post.objects.filter(branch=user_branch)

    # sort wrt to most recent
    post = post.order_by('-created_at')
    
    # Annotate each post with its comment count using a subquery
    posts = post.annotate(
        comment_count=Subquery(
            PostComment.objects.filter(post_id=OuterRef('post_id'))
            .values('post_id')
            .annotate(count=Count('comment_id'))
            .values('count')[:1]
        )
    )
    context={'post':posts,"name":"My Feed"}
    return render(request, 'post/feed.html',context)


# create an api call to add comments
@login_required(login_url='/account/login')
def add_comment(request,slug=None):
    username=request.user.__str__()
    if request.method == 'POST':
        comment = request.POST.get('comment')
        post = Post.objects.get(slug=slug)
        c = PostComment()
        c.user=request.user
        c.comment=comment
        c.post=post
        c.save()
        messages.success(request, "Comment successfully added!")
        return redirect("/post/"+slug)

        

    

@login_required(login_url='/account/login')
def tag_post(request,slug):
    username=request.user.__str__()
    try:
        # get tag
        tag = Tag.objects.get(slug=slug)
        # get posts
        post = Post.objects.filter(tags__name__in=[tag])
        # sort wrt to most recent
        post = post.order_by('-created_at')
        
        # Annotate each post with its comment count using a subquery
        posts = post.annotate(
            comment_count=Subquery(
                PostComment.objects.filter(post_id=OuterRef('post_id'))
                .values('post_id')
                .annotate(count=Count('comment_id'))
                .values('count')[:1]
            )
        )

        context={'post':posts,"name":"Tag: "+tag.name}
        return render(request, 'post/feed.html',context)
    except:
        messages.error(request, "No posts found for this tag.")
        return redirect("/error404")


@login_required(login_url='/account/login')
def post_detail(request,slug=None):
    username=request.user.__str__()
    try:    
        post=Post.objects.get(slug=slug)   
        # get comments
        comments = PostComment.objects.filter(post=post) 
        comments = comments.order_by('-created_at')

        context={'post':post,'comments':comments}
        return render(request,'post/post_detail.html',context)
    except:
        messages.error(request, "No post found")
        return redirect("/error404")

