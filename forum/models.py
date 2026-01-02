from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="threads"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="threads"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="threads"
    )

    is_locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("lock_thread", "Can lock threads"),
        ]

    def __str__(self):
        return self.title
    
    
class Reply(models.Model):
    thread = models.ForeignKey(
        "Thread",
        on_delete=models.CASCADE,
        related_name="replies"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    content = models.TextField()

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        permissions = [
            ("delete_any_reply", "Can delete any reply"),
        ]

    def __str__(self):
        return f"Reply by {self.author} on {self.thread}"
