from django.core.exceptions import PermissionDenied

def check_role_is_store_owner(user):
    return user.is_authenticated and user.role.role_name == "StoreOwner"

def check_role_is_store_owner_and_cashier(user):
    if user.is_authenticated and (user.is_superuser or (user.role.role_name == "StoreOwner" or user.role.role_name == "LocalAdmin")):
        return True
    else:
        raise PermissionDenied

def check_role_is_app_user_and_cashier(user):
    if user.is_authenticated and (user.is_superuser or (user.role.role_name == "PortalUser" or user.role.role_name == "LocalAdmin")):
        return True
    else:
        raise PermissionDenied

def check_role_is_local_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role.role_name == "AppUser")
