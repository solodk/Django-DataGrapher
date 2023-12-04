from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect

import json

from .forms import GraphForm, ProjectForm
from .models import Project, Table, Graph
from .utils import generate_plot

# Create your views here.

def index(request):
    return render(request, 'dg_app/index.html')

@login_required()
def home(request):
    graphs = Graph.objects.filter(owner=request.user).order_by('date_created')
    
    context = {'graphs': graphs}
    return render(request, 'dg_app/home.html', context)

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
        table.content = data['content']
        table.name = data['name']
        table.save()

        return JsonResponse({
            'status': 'success', 
            'redirect_url': reverse('dg_app:table', kwargs={'table_id': table.id, 'project_id': project_id})
        })

    context = {
        'content': table.content,
        'name': table.name, 
        'table_id': table_id, 
        'project_id': project_id
        }
    return render(request, 'dg_app/edit_table.html', context)

@csrf_protect
@login_required
def create_table(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        # Create a new table instance
        table = Table.objects.create(
            owner=request.user, #wrong
            project=project, 
            content=data['content'],
            name=data['name'],
        )

        return JsonResponse({
            'status': 'success', 
            'redirect_url': reverse(
                'dg_app:table', 
                kwargs={
                    'table_id': table.id, 
                    'project_id': project_id
                }
            )
        })

    context = {'project_id': project_id}
    return render(request, 'dg_app/create_table.html', context)

def create_graph(request):
    table_id = request.GET.get('table_id')
    if request.method == 'POST':
        form = GraphForm(request.POST, table_id=table_id)
        if form.is_valid():
            graph_instance = form.save(commit=False)
            graph_instance.table_id = table_id
            graph_instance.owner = request.user
            graph_instance.save()

            return redirect('dg_app:graph', graph_id=graph_instance.id)
    else:
        form = GraphForm(table_id=table_id)

    context = {'form': form, 'table_id': table_id}
    return render(request, 'dg_app/create_graph.html', context)

def graph(request, graph_id):
    graph = get_object_or_404(Graph, id=graph_id)

    graph_image = generate_plot(
        graph.table.id,
        graph.x_axis, 
        graph.y_axis, 
        graph.graph_type
        )
    context = {'graph_image': graph_image}
    return render(request, 'dg_app/graph.html', context)

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_instance = form.save(commit=False)
            project_instance.owner = request.user
            project_instance.save()
        
        return redirect('dg_app:projects')
    else:
        form = ProjectForm()
    
    context = {'form': form}
    return render(request, 'dg_app/create_project.html', context)