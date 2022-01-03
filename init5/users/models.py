from django.db import models
from django.core import validators
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
    BaseUserManager,
)


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
    ROLE = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]

    email = models.EmailField(max_length=254, db_index=True, validators=[validators.validate_email], unique=True)
    username = models.CharField(max_length=25,unique=True)
    date_registration = models.DateTimeField(verbose_name='date registration', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    role = models.CharField(max_length=100, choices=ROLE, default=USER, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    is_newsmaker = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.username}'
    
    def __call__(self):
        return self

    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('id', )
