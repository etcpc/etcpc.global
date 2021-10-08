from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Post(models.Model):
    # class Published(models.Manager):
    #     def get_queryset(self):
    #         return super().get_queryset().filter(status="published")

    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=250)

    slug = models.SlugField(max_length=250, unique_for_date="publish_date")

    image = models.ManyToManyField(
        "PostImage",  verbose_name="post_image")

    banner = models.ImageField(upload_to="Posts/images/")

    publish_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    content = models.TextField()

    status = models.CharField(
        max_length=10, choices=options, default="published")

#    / published = Published()

    def get_absolute_url(self):
        return reverse("blog:post_single", args=[self.slug])

    class Meta:
        ordering = ("-publish_date",)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    image = models.ImageField(upload_to="Posts/images/")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
