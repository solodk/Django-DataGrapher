from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import json

from .models import Project, Table

# Create your views here.

def index(request):
    return render(request, 'dg_app/index.html')

@login_required()
def home(request):
    return render(request, 'dg_app/home.html')

@login_required
def projects(request):
    projects = Project.objects.filter(owner=request.user).order_by('date_created')
    context = {'projects': projects}
    return render(request, 'dg_app/projects.html', context)

@login_required
def project(request, project_id):
    project = Project.objects.get(id=project_id)
    tables = Table.objects.filter(project=project).order_by('date_created')

    if project.owner != request.user:
        raise Http404
    
    context = {'project': project, 'tables': tables, 'project_id': project_id}
    return render(request, 'dg_app/project.html', context)

@login_required
def table(request, table_id, project_id):
    table = Table.objects.get(id=table_id)
    content = table.content

    if table.project.owner != request.user:
        raise Http404
    
    context = {'content': content, 'table_id': table_id, 'project_id': project_id}
    return render(request, 'dg_app/table.html', context)

@csrf_protect
@login_required
def edit_table(request, table_id, project_id):
    table = get_object_or_404(Table, id=table_id)

    if table.project.owner != request.user:
        raise Http404

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        # Update the existing table content
        table.content = data
        table.save()

        return JsonResponse({
            'status': 'success', 
            'redirect_url': reverse('dg_app:table', args=[table.id, project_id])
        })

    context = {'content': table.content, 'table_id': table_id, 'project_id': project_id}
    return render(request, 'dg_app/edit_table.html', context)

@csrf_protect
@login_required
def create_table(request, project_id):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        # Create a new table instance
        table = Table.objects.create(project=your_project_instance, content=data)

        return JsonResponse({
            'status': 'success', 
            'redirect_url': reverse('dg_app:table', args=[table.id, project_id])
        })

    context = {'project_id': project_id}
    return render(request, 'dg_app/create_table.html', context)