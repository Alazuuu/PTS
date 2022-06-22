from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.contrib.auth.models import PermissionsMixin


class MYUserManager(BaseUserManager):
    def create_user(self, first_name,  middle_name, last_name, email, password, phone_number):
        if not email:
            raise ValueError('user must have email address')
        user = self.model(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=self.normalize_email(email),
            phone_number=phone_number

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name,  middle_name, last_name, email, password, phone_number):
        user = self.create_user(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number
        )
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Staff(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=13)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',
                       'middle_name', 'last_name', 'phone_number']

    objects = MYUserManager()

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


# PTS USERS
class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    tag_id = models.CharField(max_length=12, unique=True)
    phone_number = models.CharField(
        max_length=13, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    balance = models.FloatField(default=0)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'
