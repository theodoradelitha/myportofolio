from django.forms.models import ModelForm
from django.forms.widgets import TextInput, Textarea, URLInput

from main.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Project Name",
            "description": "Project Description",
            "tech_stack": "Tech Stack Used",
            "project_url": "Project URL",
            "project_image_url": "Project Image URL"
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Insert your project name",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell us about your proejct",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://..."
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://"
                }
            ),
        }