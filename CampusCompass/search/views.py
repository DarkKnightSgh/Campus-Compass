# Create your views here.

from django.shortcuts import render
from django.db.models import Q
from itertools import chain

# load models

from post.models import Post
from resource.models import Resource
from account.models import Mentor,Student
from announcement.models import Announcement
from taggit.models import Tag

import re

def clean_query(q):
    if q==None:
        return None
    # remove all special character except space
    q = re.sub(r'[^a-zA-Z0-9\s]', '', q)
    # replace all space with -
    q = q.lower()
    q = re.sub(r'\s', '-', q)
    return q

def search_view(request):
    query = request.POST.get('q', None)
    # query=clean_query(query)
    
    if query is not None:
        # print(query)
        try:
            post_results = Post.objects.search(query)
        except:
            post_results = Post.objects.none()
        try:
            resource_results = Resource.objects.search(query)
        except:
            resource_results = Resource.objects.none()
        
        
        try:
            announcement_results = Announcement.objects.search(query)
        except:
            announcement_results = Announcement.objects.none()
        
        try:
            student_results = Student.objects.search(query)
        except:
            student_results = Student.objects.none()
            
        # print(post_results)
        # print(resource_results)
        # print(announcement_results)
        # print(student_results)
    
        queryset_chain = chain(
            post_results,
            resource_results,
            announcement_results,
            student_results,
        )
    
        # Sort by primary key in descending order
        qs = list(queryset_chain)
        count = len(qs)
        print(qs)
    else:
        qs = []
        count = 0

    context = {
        'query': query,
        'count': count,
        'results': qs,
    }

    return render(request, 'search/search.html', context)
    
    