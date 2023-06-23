from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Your additional fields here
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)

# class UserManager(BaseUserManager):
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, username, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=50)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.email	



class IntakeForm(models.Model):
    state = models.CharField(max_length=2)
    requestor_type = models.CharField(max_length=20)
    request_type = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    request_details = models.TextField(blank=True)
    last_4_ssn = models.CharField(max_length=4, blank=True)
    employee_id = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"IntakeForm {self.id}"

class Request(models.Model):
    name = models.CharField(max_length=100)
    request_type = models.CharField(max_length=20)
    email = models.EmailField()
    days_left = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id}"

class Event(models.Model):
    name = models.CharField(max_length=100)
    request = models.ForeignKey(Request, related_name='events', on_delete=models.CASCADE)

    def __str__(self):
        return f"Event {self.id}"

class Template(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Template {self.id}"
