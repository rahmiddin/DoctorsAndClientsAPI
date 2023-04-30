from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime


# Create your models here.


class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ Extending the AbstractUser class """
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'

    email = models.EmailField(gettext_lazy('email address'), unique=True)
    number = PhoneNumberField(unique=True)
    username = models.CharField(max_length=150, unique=False)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    category = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.category}'


class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    category = models.ManyToManyField(to=Category, related_name='categories')
    experience = models.PositiveIntegerField()
    education = models.CharField(max_length=250)
    work_time_start = models.TimeField(default='8:00')
    work_time_end = models.TimeField(default='21:00')

    class Meta:
        verbose_name = 'doctor'
        verbose_name_plural = 'doctors'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def work_status_now(cls, str_time: str, doctor_id: int) -> bool:
        doctor = Doctor.objects.get(id=doctor_id)
        right_time = datetime.strptime(str_time, '%H:%M').time()
        if doctor.work_time_end > right_time >= doctor.work_time_start:
            return True
        else:
            return False


class Service(models.Model):
    name = models.CharField(max_length=256)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE,
                                 related_name='service_category')

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return f'{self.name}'


class DoctorsService(models.Model):
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Doctor service'
        verbose_name_plural = 'Doctore services'

    def __str__(self):
        return f'{self.doctor} {self.service}'


APPOINTMENT_CHOICES = (
    ('confirmed', 'Подтвержден'),
    ('canceled', 'Отменено')
)


class Appointment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='appointment_client')
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE,
                               related_name='appointment_doctor')
    service = models.ForeignKey(to=Service, on_delete=models.CASCADE,
                                related_name='appointment_service')
    created_time = models.DateTimeField(auto_now_add=True)
    appointment_time = models.DateTimeField()
    price = models.PositiveIntegerField(null=True)
    status = models.CharField(choices=APPOINTMENT_CHOICES, default='confirmed', max_length=20)

    class Meta:
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'

    def __str__(self):
        return f'Клиент {self.user} к доктору  {self.doctor} на {self.appointment_time}'

    def save_price(self, service_id: int):
        price = Service.objects.get(id=service_id).price
        self.price = price
        self.save()

