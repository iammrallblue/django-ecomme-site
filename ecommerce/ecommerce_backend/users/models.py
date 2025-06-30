from django.db import models
from django.contrib.auth.models import AbstractUser

# Create Users model


class User(AbstractUser):

    """
    Extending Django's built-in User model with additional fields:
    - gender: Gender selection (Male, Female, Other)
    - dob: Date of Birth
    - role: User role (Admin, Customer, Staff, Guest)
    """

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('guest', 'Guest')
    )

    # Add additional fields to User model, gender, dob, role
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    # User role with default set to "customer"
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='customer')

    # Fix conflict with Django's built-in User model groups field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_groups",
        blank=True,
    )

    # Fix conflict with Django's built-in User model user_permissions field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        # Avoids conflict with Django's built-in User model user_permissions field
        related_name="custom_user_permissions",
        blank=True
    )

    def __str__(self):
        return self.username
