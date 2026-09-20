from django.urls import path
from main.views import (
    show_main, show_experience, show_projects, show_blog,
    create_project, get_projects_json, delete_project, update_project,
    create_blog, get_blogs_json, delete_blog, update_blog
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('experience/', show_experience, name='show_experience'),
    
    path('projects/', show_projects, name='show_projects'),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/update/", update_project, name="update_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),

    path('blog/', show_blog, name='show_blog'),
    path("blog/add/", create_blog, name="create_blog"),
    path("api/blog/", get_blogs_json, name="get_blogs_json"),
    path("blog/<uuid:blog_id>/update/", update_blog, name="update_blog"),
    path("blog/<uuid:blog_id>/delete/", delete_blog, name="delete_blog"),
]