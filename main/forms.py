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
            "demo_link",
            "image",
        ]

        labels = {
            "title": "Project Name",
            "description": "Project Description",
            "tech_stack": "Tech Stack Used",
            "demo_link": "Project URL",
            "image": "Project Image URL"
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
                    "placeholder": "Tell us about your project",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "demo_link": URLInput(
                attrs={
                    "placeholder": "https://..."
                }
            ),
            "image": URLInput(
                attrs={
                    "placeholder": "https://"
                }
            ),
        }