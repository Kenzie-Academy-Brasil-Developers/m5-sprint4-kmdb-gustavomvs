from lib2to3.pytree import Base
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("This field is required.")

        email = self.normalize_email(email)

        user = self.model(email=email, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
        return self._create(email=email, password=password, is_staff=True, is_superuser=False,**extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create(email=email, password=password, is_staff=True, is_superuser=True,**extra_fields)

