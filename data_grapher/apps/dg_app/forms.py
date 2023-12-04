from django import forms
from .models import Table, Project, Graph

class GraphForm(forms.ModelForm):
    

    def __init__(self, *args, **kwargs):
        table_id = kwargs.pop('table_id', [])

        super(GraphForm, self).__init__(*args, **kwargs)
        choices = self.getChoices(table_id)

        self.table = Table.objects.get(id=table_id)
        self.fields['y_axis'] = forms.ChoiceField(choices=choices)
        self.fields['x_axis'] = forms.ChoiceField(choices=choices)
        
    def getChoices(self, table_id):
        table = Table.objects.get(id=table_id)
        columns = table.content['columns']
        choices = [(index, column) for index, column in enumerate(columns)]
        return choices
    
    class Meta:
        model = Graph
        fields = ['name', 'graph_type', 'y_axis', 'x_axis']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']