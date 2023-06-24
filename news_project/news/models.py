from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

content_type = ContentType.objects.get_for_model(Post)
permission_add_post = Permission.objects.create(
    codename='add_post',
    name='Can add post',
    content_type=content_type,
)
permission_change_post = Permission.objects.create(
    codename='change_post',
    name='Can change post',
    content_type=content_type,
)

authors_group = Group.objects.get(name='authors')
authors_group.permissions.add(permission_add_post)
authors_group.permissions.add(permission_change_post)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.user.username


class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='news_user_groups',
        related_query_name='news_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='news_user_permissions',  # добавлен related_name
        related_query_name='news_user',
    )

    def __str__(self):
        return self.username

class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    content = models.TextField(default='')

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class NewsPermission(Permission):
    class Meta:
        proxy = True
        verbose_name = 'news permission'
        verbose_name_plural = 'news permissions'