from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ImproperlyConfigured
from rest_framework.response import Response
from rest_framework import status
from auth_core.serializers import *
from auth_core.models import *
from hrm.models import Employee
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView, TokenRefreshView as BaseTokenRefreshView
from auth_core.management.commands.roles import Roles
# Create your views here.

INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"

class CreateUserView(CreateAPIView):
    serializer_class = UserSerializerWithToken

    #Link the newly created user to employee record
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # role = serializer.validated_data.pop('role')
        role = Roles.EMPLOYEE.value
        errors = {}
        if role != Roles.ADMIN.value:
            try:
                phone_num = serializer.validated_data.pop('phone_num')
                employee = Employee.objects.get(emp_phone_num = phone_num)
                role_group = Group.objects.get(name=role)

                user = serializer.save()
                employee.user = user
                user.groups.add(role_group)
                employee.save()
            except Employee.DoesNotExist as e:
                errors.update({'phone_num': 'Phone number did not match any Employee records. Please try again'})
            except Group.DoesNotExist as e:
                errors.update({'role': role+' role does not exists in database'})
            except Exception as e:
                errors.update({'errors': str(e)})
            
            
        else:
            user = serializer.save()
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    site_name = '/auth/reset'
    email_template_name = "auth/password_reset_email.html"
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    subject_template_name = "auth/password_reset_subject.txt"
    token_generator = default_token_generator

    def post(self, request, *args, **kwargs):
        opts = {
            "site_name": self.site_name,
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        try:
            password_reset_serializer = self.get_serializer(data=request.data)
            password_reset_serializer.is_valid(raise_exception=True)
            password_reset_serializer.save(**opts)

            return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_202_ACCEPTED)
        
        except Exception as e:
            return Response({'email': str(e)}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(GenericAPIView):
    serializer_class = SetPasswordSerializer
    lookup_field = 'uidb64'
    reset_url_token = 'set-password'
    token_generator = default_token_generator


    def link_validation(self, uidb64, token):
        errors = {}
        validlink = False
        user = self.get_object(uidb64)

        if user is not None:
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(user, session_token):
                    # If the token is valid, display the password reset form.
                    validlink = True
                    return validlink, errors, user
            else:
                if self.token_generator.check_token(user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    validlink = True
                    return validlink, errors, user
                    
            errors.update({'token': 'Token cannot be verified, link is invalid'})
        else:
            errors.update({'user': 'User is not found. Password reset failed'})
        return validlink, errors, user
    
    def get_context_data(self, **kwargs):
        context = {}
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    "form": None,
                    "title": _("Password reset unsuccessful"),
                    "validlink": False,
                }
            )
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if "uidb64" not in self.kwargs or "token" not in self.kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user
    
    def post(self, request, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        validlink, errors, user = self.link_validation(uidb64, token)
        if validlink and not errors:
            try:
                set_password_serializer = self.get_serializer(data=request.data, context={'user': user})
                set_password_serializer.is_valid(raise_exception=True)
                user = set_password_serializer.save()
                del self.request.session[INTERNAL_RESET_SESSION_TOKEN]

                return Response({'message': 'Password is reset successfully'}, status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    #to check if uidb64 and token is valid, and decide whether to show the reset form
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']

        #check if link submitted is valid
        validlink, errors, _ = self.link_validation(uidb64, token)
        
        if validlink and not errors:
            if token == self.reset_url_token:
                return Response({'validlink': validlink}, status=status.HTTP_202_ACCEPTED)
            else:
                self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    ).replace('/api', '')

                return Response({'validlink': validlink, 'redirect_url': redirect_url}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
      
    
class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.Serializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class UserView(RetrieveUpdateAPIView):
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
