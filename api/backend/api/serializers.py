from rest_framework.serializers import ModelSerializer


from .models import User


class UserSerializer(ModelSerializer):
    """ Serializer for user model """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'number', 'email', 'password')
