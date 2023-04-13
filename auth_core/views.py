from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status
from auth_core.serializers import *
from auth_core.models import *
from hrm.models import Employee
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView, TokenRefreshView as BaseTokenRefreshView
from auth_core.management.commands.roles import Roles

# Create your views here.

class CreateUserView(CreateAPIView):
    serializer_class = UserSerializerWithToken

    #Link the newly created user to employee record
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # role = serializer.validated_data.pop('role')
        role = Roles.EMPLOYEE.value
        if role != Roles.ADMIN.value:
            try:
                phone_num = serializer.validated_data.pop('phone_num')
                employee = Employee.objects.get(emp_phone_num = phone_num)
                role_group = Group.objects.get(name=role)
            except (Employee.DoesNotExist, Group.DoesNotExist) as e:
                return Response({'error': str(e)+', please try again.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()
            employee.user = user
            user.groups.add(role_group)
            employee.save()
        else:
            user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.Serializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializerWithToken
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class TokenRefreshView(BaseTokenRefreshView):
    pass

class GetUserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerWithToken
    permission_classes = [IsAdminUser, IsAuthenticated]
