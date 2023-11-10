from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import *

class StoreOwnerBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        email = kwargs['username']
        password = kwargs['password']
        try:
            organisation_admin = StoreOwner.objects.get(user__email=email)
            print(organisation_admin.user.password)
            if organisation_admin and check_password(password, organisation_admin.user.password) is True:
                return organisation_admin.user.pk
        except StoreOwner.DoesNotExist:
            pass

class CashierBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        email = kwargs['username']
        password = kwargs['password']
        try:
            local_admin = Cashier.objects.get(user__email=email)
            if local_admin and check_password(password, local_admin.user.password) is True:
                return local_admin.user.pk
        except Cashier.DoesNotExist:
            pass

class AppUserBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        email = kwargs['username']
        password = kwargs['password']
        try:
            security_personnel=AppUser.objects.get(user__email=email)
            if security_personnel and check_password(password, security_personnel.user.password) is True:
                return security_personnel.user.pk
        except AppUser.DoesNotExist:
            pass