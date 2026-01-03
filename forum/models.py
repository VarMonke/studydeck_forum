from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)   # CS F111
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Resource(models.Model):
    RESOURCE_TYPES = [
        ("pdf", "PDF"),
        ("video", "Video"),
        ("link", "Link"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="resources"
    )

    title = models.CharField(max_length=200)
    resource_type = models.CharField(
        max_length=10,
        choices=RESOURCE_TYPES
    )
    link = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
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

    resources = models.ManyToManyField(
        Resource,
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
    
    def score(self):
        return self.votes.aggregate(total=models.Sum("value"))["total"] or 0 #type: ignore
    
    def user_vote(self, user):
        if not user.is_authenticated:
            return 0
        
        vote = self.votes.filter(user=user).first() #type: ignore
        
        return vote.value if vote else 0
    
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
    
    def score(self):
        return self.votes.aggregate(total=models.Sum("value"))["total"] or 0 #type: ignore
    
    def user_vote(self, user):
        if not user.is_authenticated:
            return 0
        
        vote = self.votes.filter(user=user).first() #type: ignore
        return vote.value if vote else 0


class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1

    VOTE_CHOICES = (
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="votes",
    )

    thread = models.ForeignKey(
        "Thread",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="votes",
    )

    reply = models.ForeignKey(
        "Reply",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="votes",
    )

    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "thread"],
                name="unique_user_thread_vote",
            ),
            models.UniqueConstraint(
                fields=["user", "reply"],
                name="unique_user_reply_vote",
            ),
        ]



class Report(models.Model):
    TARGET_CHOICES = [
        ("thread", "Thread"),
        ("reply", "Reply"),
        ("resource", "Resource"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("resolved", "Resolved"),
    ]

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports"
    )

    target_type = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES
    )

    target_id = models.PositiveIntegerField()

    reason = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report #{self.id} ({self.target_type}:{self.target_id})" #type: ignore
    

    def get_target_url(self):
        if self.target_type == "thread":
            return reverse("thread_detail", args=[self.target_id])

        if self.target_type == "reply":
            # reply belongs to a thread
            from forum.models import Reply
            reply = Reply.objects.filter(id=self.target_id).first()
            if reply:
                return (
                    reverse("thread_detail", args=[reply.thread.id])
                    + f"#reply-{reply.id}" #type: ignore
                )

        return "#"





