from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, GroupManager as BaseGroupManager, Group as BaseGroup
    
class UserManager(BaseUserManager):
    def create_user(self, username, email, name, password=None, **extra_fields):
        if not email or not username:
            raise ValueError("User must have an email address and username")
        user = self.model(username=username, email=self.normalize_email(email), name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, email, name, password):
        user = self.create_user(username, email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name', 'role']

class GroupManager(BaseGroupManager):
    pass

class Group(BaseGroup):
    pass
