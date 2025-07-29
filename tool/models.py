from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = ManyToManyField(Category, related_name='tools')
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tools_owner')
    image = models.ImageField(upload_to='uploads/tool/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"