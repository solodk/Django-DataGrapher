from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
    
    context = {'project': project, 'tables': tables}
    return render(request, 'dg_app/project.html', context)

@login_required
def table(request, table_id):
    table = Table.objects.get(id=table_id)
    content = table.content

    if table.project.owner != request.user:
        raise Http404
    
    context = {'content': content}
    return render(request, 'dg_app/table.html', context)