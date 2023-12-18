"""
Custom user models.
"""
import uuid
import os
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from core.fields import OrderField


def profile_image_file_path(instance, filename):
    """Generating a file path for a new profile image."""
    ext = os.path.splitext(filename)[1]
    unique_name = uuid.uuid4()
    filename = f'{unique_name}{ext}'

    path = os.path.join('uploads', 'profile', filename)
    return path


class CustomUserManager(BaseUserManager):
    """Custom manager for the user model."""
    def create_user(self, email, password=None, **kwargs):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError(_('Email must be set...'))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password) :
        """Create and return a new superuser with the given email and password."""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for using email instead of username."""
    email = models.EmailField(
        _('Email address'), max_length=100, unique=True
    )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def _str_(self) :
        return self.email
    
SEX = [
    ("M", "male"),
    ("F","female")
]


class Profile(models.Model):
    """This class defines attributes of the Profile model."""
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=200)
    bio = models.TextField(max_length=1000)
    sex = models.CharField(choices=SEX, max_length=6)

    def __str__(self):
        return self.user.email


class ProfileImage(models.Model) :
    """This class defines attributes of the ProfileImage model."""
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='profile_image'
    )
    url = models.ImageField(
        upload_to=profile_image_file_path, null=True, default='test.jpg'
    )
    order = OrderField(unique_for_field="profile", blank=True)

    def clean(self):
        """Validating multiple fields with clean_fields
        method for preventing from inserting duplicate values."""
        queryset = ProfileImage.objects.filter(
            profile=self.profile
        )
        for object in queryset:
            if self.id != object.id and self.order == object.order:
                raise ValidationError('Duplicate value.')

    def save(self, *args, **kwargs) :
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.profile.user.email}: {self.url}'

# ======= Signal for creating profile after saving new users in db =======
@receiver (post_save, sender=User)
def save_profile (sender, instance, created, **kwargs) :
    if created:
        Profile.objects.create(user=instance)