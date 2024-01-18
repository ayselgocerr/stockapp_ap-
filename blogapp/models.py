from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):

    name = models.CharField(max_length=100)


    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categorys"

    def __str__(self):
        return f"{self.name}"


class Blog(models.Model):

    STATUS = (("D", "Draft"),
             ("P", "Published"))

    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    image = models.CharField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, models.PROTECT, related_name="BlogCategory")
    publish_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.PROTECT, related_name="UserBlog")
    status = models.CharField(max_length=1, choices=STATUS, blank=True, null=True)

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = "blogs"

    def __str__(self):
        return f"{self.title} - {self.category} - {self.status} - {self.user}"




class Comment(models.Model):
    user = models.ForeignKey(User, models.PROTECT, related_name = "UserComment")
    time_stamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=200, blank=True, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name = "BlogComment")

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"{self.time_stamp} - {self.content} - {self.user}"



class PostView(models.Model):
    user = models.ForeignKey(User, models.PROTECT, related_name = "UserPostViews")
    post_views = models.BooleanField(default=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name = "BlogPostViews")
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "postview"
        verbose_name_plural = "postviews"

    def __str__(self):
        return f"{self.time_stamp} - {self.post_views} - {self.user}"


class Like(models.Model):
    user = models.ForeignKey(User, models.PROTECT, related_name = "UserLikes")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name = "BlogLikes")
    likes = models.BooleanField(default=True)

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"

    def __str__(self):
        return f"{self.user} - {self.blog} - {self.likes}"