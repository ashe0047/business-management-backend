import unicodedata
from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import forms
from django.template import loader
from drf_spectacular.utils import extend_schema_field
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from drf_spectacular.types import *
from auth_core.management.commands.roles import Roles
from auth_core.models import User

#helper function
UserModel = get_user_model()
def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return (
        unicodedata.normalize("NFKC", s1).casefold()
        == unicodedata.normalize("NFKC", s2).casefold()
    )
class UserSerializer(serializers.ModelSerializer):
    # role = serializers.CharField(read_only=True, default=Roles.EMPLOYEE.value)
    phone_num = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel    
        fields = ['username', 'email', 'name', 'password', 'phone_num']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

    def create(self, validated_data):
        # validated_data.pop('token')
        return UserModel.objects.create_user(**validated_data)

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
        model = UserModel
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
        
        serializer = UserSerializer(self.user).data
        user_data = {k:v for k, v in serializer.items()}
        data.update(user_data)

        return data

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False, max_length=254, required=True)

    def validate_email(self, value):
        try:
            user = UserModel.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email address does not exist.')
        return value

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(
        self,
        domain_override=None,
        site_name=None,
        subject_template_name="password_reset_subject.txt",
        email_template_name="password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        email = self.validated_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            # site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )

class SetPasswordSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=6, max_length=128, write_only=True, required=True)
    password2 = serializers.CharField(min_length=6, max_length=128, write_only=True, required=True)

    def validate(self, value):
        password1 = value.get('password1', None).strip()
        password2 = value.get('password2', None).strip()
        if password1 != password2:
            raise ValidationError('Passwords does not match')
        password_validation.validate_password(password2, self.context.get('user', None))
        return value
    
    def save(self, **kwargs):
        password = self.validated_data["password1"]
        user = self.context.get('user', None)
        user.set_password(password)
        user.save()
        return user
    
    
    class Meta:
        model = UserModel
        exclude = ('username', 'email', 'name', 'password')
class PasswordResetConfirmSerializer(serializers.Serializer):
    validlink = serializers.BooleanField()
    redirect_url = serializers.CharField(required=False)

    class Meta:
        read_only_fields = ('validlink', 'redirect_url',)

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
    