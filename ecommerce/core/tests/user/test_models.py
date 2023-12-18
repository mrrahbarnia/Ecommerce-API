"""
Test users models.
"""
import pytest

from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from core.models.user import (
    Profile,
    ProfileImage
)

pytestmark = pytest. mark.django_db
User = get_user_model ()


class TestUserModel:
    """Tests for the user model."""
    def test_create_user_with_email_successfully(self, create_user):
        """Test creating user with the provided email successfully."""
        email = 'Test@example.com'
        password = 'Test123456'
        obj = create_user

        assert obj.email == email
        assert obj.check_password(password) == True

    def test_create_user_with_normalized_email(self) :
        """Test creating a user model instance
        with the normalized email option."""
        sample_emails = [
            ('Test1@test.email','Test1@test.email'),
            ('TEST2@test.email','TEST2@test.email'),
            ('Test3@TEST.email', 'Test3@test.email'),
            ('Test4@test.EMAIL','Test4@test.email')
        ]

        for email, expected in sample_emails:
            obj = User.objects.create_user(
                email=email, password= 'Test12345'
            )
            assert obj.email == expected

    def test_create_user_unique_email_constraint (self, create_user) :
        """Test creating user with the unique constraint on email field."""
        obj = create_user
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email=obj.email, password='Test12345'
            )

    def test_max_length_email_field(self):
        """Test the max_length option for the email field."""
        email = 'e' * 101
        obj = User.objects.create_user(
            email=email, password='Test12345'
        )

        with pytest.raises(ValidationError):
            obj.full_clean()
    
    def test_str_method(self, create_user):
        """Test the _str_ method."""
        obj = create_user

        assert str(obj) == obj.email

    def test_create_super_user_method (self, create_superuser):
        """Test the create_superuser method."""
        obj = create_superuser

        assert obj.is_superuser == True
        assert obj.is_staff== True

    
    class TestProfileModel:
        """Tests for the Profile model."""
        def test_str_method_and_signal_works_successfully(self, create_user):
            """Test the _str_ method and the provided signal for the Profile module"""
            user_obj = create_user
            profile_obj = Profile.objects.get(user=user_obj)

            assert str(profile_obj) == user_obj.email

    class TestProfileImageModel:
        """Tests for the ProfileImage model."""
        def test_str_method(self):
            """Test the _str_ method for the ProfileImage model."""
            user_obj = get_user_model().objects.create_user(
                email= 'Test@example.com', password= 'Test12345'
            )
            profile_obj = Profile.objects.get(user=user_obj)
            obj = ProfileImage.objects.create(profile=profile_obj)
            assert str(obj) == f'{user_obj.email}: {obj.url}'
        
        def test_order_field_duplicate_value (self):
            """Test preventing to inserting duplicate value for the order field."""
            user_obj = get_user_model().objects.create_user(
                email='Test@example.com', password='Test12345'
            )
            profile_obj = Profile.objects.get(user=user_obj)
            obj = ProfileImage.objects.create(profile=profile_obj)
            assert str(obj) == f'{user_obj.email}: {obj.url}'

        def test_order_field_duplicate_value (self) :
            """Test preventing to inserting duplicate value for the order field."""
            user_obj = get_user_model().objects.create_user(
                email='Test@example.com', password='Test12345'
            )
            profile_obj = Profile.objects.get(user=user_obj)
            ProfileImage.objects.create(profile=profile_obj, order=1)
            ProfileImage.objects.create(profile=profile_obj, order=2)
            with pytest.raises(ValidationError):
                ProfileImage.objects.create(profile=profile_obj, order=1)
