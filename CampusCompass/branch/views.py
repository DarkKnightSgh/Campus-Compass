from django.shortcuts import render

from .models import Branch
from django.http import JsonResponse

# Create your views here.

def get_branches(request, department_id):
    branches = {}
    if (Branch.objects.filter(department_id=department_id).exists()):
        branches = Branch.objects.filter(department_id=department_id).values('branch_code', 'branch_name')
    return JsonResponse({'branches': list(branches)})