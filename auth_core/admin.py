from django.contrib import admin
from django import forms
from django.forms import ModelChoiceField, IntegerField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group as BaseGroup
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm,  UserCreationForm as BaseUserCreationForm
from auth_core.models import *
from hrm.models import Employee
from django.utils.translation import gettext_lazy as _
from config.utils import get_config_value
from config.enums import ConfigKeys

#Change admin site title
try:
    admin.site.site_header = get_config_value(ConfigKeys.COMPANY_NAME.value)+" Administration Panel"
except Exception:
    pass

# Register your models here.
class UserCreationForm(BaseUserCreationForm):
    group = ModelChoiceField(queryset=Group.objects.all())
    phone_num = IntegerField()
    
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password1', 'password2', 'group',)
    
    def get_employee(self):
        employee = None
        try:
            employee = Employee.objects.get(emp_phone_num=self.cleaned_data.get('phone_num'))
        except Employee.DoesNotExist:
            raise forms.ValidationError('Employee record not found, please check phone number')
        return employee
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        group = self.cleaned_data.get('group')
        employee = self.get_employee()
        user.save()
        if employee:
            employee.user = user
            employee.save()
        if group:
            group.user_set.add(user)
        else:
            raise forms.ValidationError("Group/Role record not found, please check if the Group/Role is valid")
        # if commit:
        #     user.save()
        
        return user

class UserChangeForm(BaseUserChangeForm):
    group = ModelChoiceField(queryset=Group.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['group'].initial = self.instance.groups.first()
    
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password', 'group',)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        group = self.cleaned_data.get('group')
        if user.pk and user.groups.exists():
                for existing_group in user.groups.all():
                    existing_group.user_set.remove(user)
        if group:   
            group.user_set.add(user)
        if commit:
            user.save()
        return user

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    ordering = ['id']
    list_display = ['username','name','email', 'get_group', 'last_login']
    def get_group(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_group.short_description = "Role"

    fieldsets = (
        (None, {'fields': ('username', 'name', 'email', 'password', 'group',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', )})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'name',
                'phone_num',
                'password1',
                'password2',
                'group',
                'is_active',
                'is_staff',
                'is_superuser', 
            )
        }),
    )

class GroupAdmin(BaseGroupAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.unregister(BaseGroup)
admin.site.register(Group, GroupAdmin)