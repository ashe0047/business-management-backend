from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema_field
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from drf_spectacular.types import *
from auth_core.management.commands.roles import Roles

class UserSerializer(serializers.ModelSerializer):
    # role = serializers.CharField(read_only=True, default=Roles.EMPLOYEE.value)
    phone_num = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = get_user_model()    
        fields = ['username', 'email', 'name', 'password', 'phone_num']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

    def create(self, validated_data):
        # validated_data.pop('token')
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        
        return user
    
    
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'name', 'password', 'phone_num', 'token']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }
    
    @extend_schema_field(OpenApiTypes.STR)
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        serializer = UserSerializerWithToken(self.user).data
        user_data = {k:v for k, v in serializer.items()}
        data.update(user_data)

        return data

    
# class AuthTokenSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         trim_whitespace = False,
#     )

#     def validate(self, attrs):
#         username =  attrs.get('username')
#         password = attrs.get('password')
#         user = authenticate(
#                     request=self.context.get('request'),
#                     username=username,
#                     password=password,
#                 )
#         return super().validate(attrs)
    