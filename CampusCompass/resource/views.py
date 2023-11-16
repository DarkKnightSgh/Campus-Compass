from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ResourceForm
from branch.models import Branch
from .models import Resource
from django.contrib.auth.models import User
from taggit.models import Tag

from django.http import HttpResponse

# Create your views here.    


login_required(login_url='/account/login')
def resource(request):
    username=request.user.__str__()
    if(username=='AnonymousUser'):
        return redirect("/account/login")
    print(request.user.student.branch)
    user_branch = request.user.student.branch 
    # Filter resources by the user's branch
    resource = Resource.objects.filter(branch= user_branch)
    # sort wrt to most recent
    resource = resource.order_by('-uploaded_at')
    context={'resources':resource}
    return render(request, 'resource/resource.html',context)

login_required(login_url='/account/login')
def resource_by_tag(request,tag):
    username=request.user.__str__()
    try:
        # get tag
        tag = Tag.objects.get(slug=tag)
        # get resources
        resource = Resource.objects.filter(tags__name__in=[tag])
        # sort wrt to most recent
        resource = resource.order_by('-uploaded_at')
        context={'resources':resource}

        return render(request, 'resource/resource.html',context)
    except:
        messages.error(request, "No resources found for this tag.")
        return redirect('/error404')

login_required(login_url='/account/login')
def upload_resource(request):
    username=request.user.__str__()
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            # get branches
            branches = form.cleaned_data['branch']
            # get tags
            tags = form.cleaned_data['tags']
            print(branches,tags)
            # get title
            title = form.cleaned_data['title']
            
            r= form.save(commit=False)
            r.user = User.objects.get(username=username)
            r.save()
            # add branches
            for branch in branches:
                r.branch.add(branch)
            # add tags
            for tag in tags:
                tag = tag.strip().lower()
                domain, created = Tag.objects.get_or_create(name=tag)
                r.tags.add(tag)

            messages.success(request, "Resource successfully added!")
            return redirect('/resource')
        else:
            messages.error(request, "Error in form submission. Please correct the errors below.")

    else:
        form = ResourceForm()
    return render(request, 'resource/upload_resource.html', {'form': form,"name":"Upload Resources"})

login_required(login_url='/account/login')
def edit_resource(request,id=None):
    username=request.user.__str__()
    # get resource
    resource = Resource.objects.get(id=id)
    # get user
    user=User.objects.get(username=username)

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid() and resource.user==user:
            # get branches
            branches = form.cleaned_data['branch']
            # get tags
            tags = form.cleaned_data['tags']
            print(branches,tags)
            
            resource.title = form.cleaned_data['title']
            # check if files
            if form.cleaned_data['files']:
                resource.files = form.cleaned_data['files']
            resource.save()
            for branch in branches:
                resource.branch.add(branch)
            resource.tags.clear()
            for tag in tags:
                tag = tag.strip().lower()
                domain, created = Tag.objects.get_or_create(name=tag)
                resource.tags.add(tag)

            messages.success(request, "Resource successfully updated!")
            return redirect('/resource')
        else:
             # Check if 'files' field is empty
            if 'files' not in form.cleaned_data:
                branches = form.cleaned_data['branch']
                # get tags
                tags = form.cleaned_data['tags']
                # No new file provided, retain the existing file
                resource.title = form.cleaned_data['title']
                resource.save()
                for branch in branches:
                    resource.branch.add(branch)
                resource.tags.clear()
                for tag in tags:
                    tag = tag.strip().lower()
                    domain, created = Tag.objects.get_or_create(name=tag)
                    resource.tags.add(tag)

                messages.success(request, "Resource successfully updated!")
                return redirect('/resource')
            else:
                messages.error(request, "Error in form submission. Please correct the errors below.")

    else:
        form = ResourceForm(instance=resource)
    return render(request, 'resource/upload_resource.html', {'form': form,"name":"Edit Resources"})

login_required(login_url='/account/login')
def delete_resource(request,id=None):
    username=request.user.__str__()
    # get resource
    resource = Resource.objects.get(id=id)
    # get user
    user=User.objects.get(username=username)
    if resource.user==user:
        resource.delete()
        messages.success(request, "Resource successfully deleted!")
        return redirect('/resource')
    else:
        messages.error(request, "You are not authorized to delete this resource.")
        return redirect('/resource')
    
login_required(login_url='/account/login')
def download_resource(request,id):
    username=request.user.__str__()
    resource = Resource.objects.get(id=id)
    # Open and read the file
    with open(resource.files.path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        
    # Set the Content-Disposition header to suggest a filename for the downloaded file
    response['Content-Disposition'] = f'attachment; filename="{resource.files.name}"'
    
    return response
    
   