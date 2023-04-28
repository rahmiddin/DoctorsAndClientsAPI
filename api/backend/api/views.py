from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError as RestValidationError
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.validators import validate_international_phonenumber

from .models import User
from .serializers import UserSerializer

# Create your views here.


class UserViewSet(viewsets.ViewSet):
    """ User viewset which fulfills: list, create, update """

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def create(self, request):
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
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    return JsonResponse({'status': 'True'})
                else:
                    return JsonResponse({'Status': 'False', 'Error': user_serializer.errors})
        else:
            return JsonResponse({'Status': 'False', 'Error': 'required data not provided'})

    def partial_update(self, request, pk=None):
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




