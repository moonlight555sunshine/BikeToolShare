from importlib.metadata import requires

from django import forms
from tool.models import Tool, Category



class ToolForm(forms.ModelForm):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    description = forms.CharField(label="",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}), required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, label="Category (one or more)")
    image = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}))

    class Meta:
        model = Tool
        fields = ['name', 'description', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            all_category = Category.objects.get(name__iexact='All Tools')
            self.fields['category'].initial = [all_category.id]

        except Category.DoesNotExist:
            raise forms.ValidationError('"All Tools" category does not exist. Please contact admin.')

    def clean_category(self):
        categories = self.cleaned_data.get('category')
        try:
            all_category = Category.objects.get(name__iexact='All Tools')
            if all_category not in categories:
                self.add_error(None, '"All Tools" must be selected.')
        except Category.DoesNotExist:
            self.add_error(None, '"All Tools" category does not exist. Please contact admin.')
        return categories