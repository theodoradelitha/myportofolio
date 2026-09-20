from django.forms.models import ModelForm
from django.forms.widgets import TextInput, Textarea, URLInput

from main.models import Project, BlogPost, Experience


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

class BlogForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "content",
            "read_time",
        ]

        labels = {
            "title": "Post Title",
            "content": "Post Content",
            "read_time": "Read Time (minutes)"
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Insert your post title",
                    "maxlength": 255,
                }
            ),
            "content": Textarea(
                attrs={
                    "placeholder": "Write your blog post here...",
                    "rows": 10,
                }
            ),
            "read_time": TextInput(
                attrs={
                    "placeholder": "e.g. 5",
                    "type": "number",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at"
        ]

        labels = {
            "title": "Role / Position",
            "description": "Experience Description",
            "category": "Category",
            "thumbnail": "Thumbnail URL",
            "ended_at": "End Date"
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Software Engineer Intern",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe what you did...",
                    "rows": 4,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://"
                }
            ),
            "ended_at": TextInput(
                attrs={
                    "type": "date",
                }
            )
        }