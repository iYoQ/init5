from django.db import models
from django.core import validators
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
    BaseUserManager,
)
from ..articles.models import Article
from ..news.models import News
from ..comments.models import ArticleComment, NewsComment


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('invalid email')
        if not username:
            raise ValueError('invalid username')
        user = self.model(
            email=self.normalize_email(email), 
            username=username, 
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_newsmaker', False)
        extra_fields.setdefault('role', User.USER)
        return self._create_user(email, username, password, **extra_fields)
    
    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_newsmaker', True)
        extra_fields.setdefault('role', User.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER = 'user'
    ADMIN = 'admin'
    ROLE = (
        (USER, 'user'),
        (ADMIN, 'admin'),
    )
    GENDER = (
        ('male', 'male'),
        ('female', 'female'),
    )

    email = models.EmailField(max_length=254, db_index=True, validators=[validators.validate_email], unique=True)
    username = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='user/avatar/', blank=True, null=True)
    rating = models.IntegerField(default=0)
    role = models.CharField(max_length=20, choices=ROLE, default=USER, null=True, blank=True)
    date_registration = models.DateTimeField(verbose_name='date registration', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_newsmaker = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.username}'
    
    def __call__(self):
        return self

    def post_count(self):
        qs_articles = Article.objects.filter(author__username=self.username).values_list('id')
        qs_news = News.objects.filter(author__username=self.username).values_list('id')
        qs_posts = qs_articles.union(qs_news)
        return qs_posts.count()

    def comments_count(self):
        qs_articles = ArticleComment.objects.filter(author__username=self.username)
        qs_news = NewsComment.objects.filter(author__username=self.username)
        qs_comments = qs_articles.union(qs_news)
        return qs_comments.count()
    
    # def get_absolute_url(self):
    #     pass
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('id', )
