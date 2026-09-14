from django.db import models
import uuid

from django.db import models

class Experience(models.Model):

    # limits category to a known set of values
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("resesarch", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    # creates a UUID primary key automatically
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time"
    )
    thumbnail = models.URLField(blank=True, default="")
    started_at = models.DateTimeField(auto_now_add=True) # records when the row is created
    ended_at = models.DateTimeField(blank=True, null=True) # may be left empty for an ongoing experience

    # gives each object a readable string representation
    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None # returns True when ended_at is empty

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200)
    demo_link = models.URLField(blank=True, null=True)
    image = models.CharField(max_length=255, default="img/blank-folder.svg")

class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    read_time = models.IntegerField(help_text="Read time in minutes")