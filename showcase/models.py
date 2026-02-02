from django.db import models

# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='projects', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='portfolio_images/')
    client_name = models.CharField(max_length=100, blank=True)
    completed_date = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, help_text="Check to show on Homepage")

    def __str__(self):
        return self.title
    

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15) 
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name}"
    

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.project.title}"
    