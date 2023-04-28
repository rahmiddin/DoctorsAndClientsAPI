from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy
# Create your models here.


class User(AbstractUser):
    """ Extending the AbstractUser class """
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    email = models.EmailField(gettext_lazy('email address'), unique=True)
    number = PhoneNumberField(unique=True)
    username = models.CharField(max_length=150, unique=False)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


