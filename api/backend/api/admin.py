from django.contrib import admin
from .models import Doctor, Category, Appointment, User, Service
# Register your models here.


@admin.register(User)
class DoctorAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        field = ('first_name', 'last_name', 'email', 'number')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    class Meta:
        model = Doctor
        field = ('first_name', 'last_name', 'age', 'category', 'experience',
                 'education', 'work_time_start', 'work_time_end')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category
        field = ('name', )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    class Meta:
        model = Appointment
        field = ('user', 'doctor', 'created_time', 'appointment_time', 'price', 'status')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    class Meta:
        model = Appointment
        field = ('name', 'category')
