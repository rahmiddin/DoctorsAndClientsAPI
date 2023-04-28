from rest_framework.serializers import ModelSerializer

from .models import User, Appointment


class UserSerializer(ModelSerializer):
    """ Serializer for user model """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'number', 'email', 'password')
        write_only = 'password'


class AppointmentSerializer(ModelSerializer):
    """ Serializer for appointment model """
    class Meta:
        model = Appointment
        fields = ('user', 'doctor', 'number', 'email', 'password')
        write_only = 'password'
