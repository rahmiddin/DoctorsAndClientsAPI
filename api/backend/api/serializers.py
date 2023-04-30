from rest_framework.serializers import ModelSerializer

from .models import User, Appointment, Doctor, Category


class UserSerializer(ModelSerializer):
    """ Serializer for user model """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'number', 'email', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CategorySerializer(ModelSerializer):
    """ Serializer for user model """

    class Meta:
        model = Category
        fields = ('id', 'category')
        read_only_fields = ('id', 'category')


class DoctorSerializer(ModelSerializer):
    """ Serializer for doctor model """

    class Meta:
        model = Doctor
        fields = ('id', 'first_name', 'last_name')


class AppointmentSerializer(ModelSerializer):
    """ Serializer for appointment model """

    class Meta:
        model = Appointment
        fields = ('id', 'user', 'doctor', 'service', 'price', 'appointment_time')
        read_only_fields = ('price', 'id')

