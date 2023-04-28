from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User, Appointment
from .serializers import UserSerializer, AppointmentSerializer

# Create your views here.


class UserViewSet(viewsets.ViewSet):
    """ User ViewSet """

    def list(self, request):
        """ Get users list """
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def retrieve(self, request, pk: int = None):
        """ Get user with pk  """
        queryset = User.objects.filter(id=pk)
        print(queryset)
        if queryset:
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        else:
            return JsonResponse({'Status': False}, status=404)

    @extend_schema(responses=UserSerializer)
    def create(self, request):
        """ Create user, validate password and phone number """
        serializer = UserSerializer(data=request.data)

        if {'last_name', 'first_name', 'email', 'number', 'password'}.issubset(request.data):
            try:
                validate_international_phonenumber(request.data['number'])
            except ValidationError:
                return JsonResponse({'Status': 'False', 'Error': 'Incorrect number'})

            try:
                validate_password(request.data['password'])
            except RestValidationError as password_errors:
                errors_array = []
                for error in password_errors:
                    errors_array.append(error)
                return JsonResponse({'Status': 'False', 'Error': {'password': errors_array}})
            else:
                if serializer.is_valid():
                    user = serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    return JsonResponse({'status': 'True'})
                else:
                    return JsonResponse({'Status': 'False', 'Error': serializer.errors})
        else:
            return JsonResponse({'Status': 'False', 'Error': 'required data not provided'})

    @extend_schema(responses=UserSerializer)
    def partial_update(self, request, pk: int = None):
        """ Update current user"""

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Login required'}, status=403)

        request_user_id = request.user.id
        user = User.objects.get(id=pk)
        if user.id == request_user_id:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(request.data['password'])
                user.save()
                return JsonResponse({'status': 'True'})
            else:
                return JsonResponse({'Status': False, 'Error': serializer.errors})
        else:
            return JsonResponse({'Status': False, 'Error': 'Forbidden'})


class CreateAppointmentView(viewsets.ViewSet):
    pass