from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project, BlogPost


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "components/experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

class ProjectTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_projects_url_and_templates(self):
        response = self.client.get(reverse('main:show_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/projects.html')

    def test_project_data_appears_when_not_empty(self):
        Project.objects.create(
            title="Test Project 123",
            description="Testing the database loop.",
            tech_stack="Django, SQLite"
        )
        response = self.client.get(reverse('main:show_projects'))
        self.assertContains(response, "Test Project 123")
        self.assertContains(response, "Django, SQLite")

    def test_empty_message_appears_when_data_is_empty(self):
        response = self.client.get(reverse('main:show_projects'))
        self.assertContains(response, "No projects have been added yet.")

class BlogPostTests(TestCase):
    def test_blog_url_and_template(self):
        # tests if the URL is accessible and uses the correct template
        response = self.client.get(reverse('main:show_blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/blog.html')

    def test_blog_data_appears_when_not_empty(self):
        # tests if model data appears in the HTML response when not empty
        BlogPost.objects.create(
            title="Test Blog Post",
            content="Testing the blog loop.",
            read_time=5
        )
        response = self.client.get(reverse('main:show_blog'))
        self.assertContains(response, "Test Blog Post")
        self.assertContains(response, "Testing the blog loop.")

    def test_empty_message_appears_when_data_is_empty(self):
        # tests that an empty message appears when there is no data
        response = self.client.get(reverse('main:show_blog'))
        self.assertContains(response, "No posts yet. I'm currently writing my first one!")