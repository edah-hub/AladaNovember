from main.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=StoreOwner)
def create_new_store_owner(sender,instance,created,*args,**kwargs):
    if created:
        records = User.objects.get(email=instance.user)
        records.role_id=instance.role
        records.save()
        print('user role updated successfully')


@receiver(post_save,sender=AppUser)
def create_new_app_user(sender,instance,created,*args,**kwargs):
    if created:
        records = User.objects.get(email=instance.user)
        records.role_id=instance.role
        records.save()
        print('user role updated successfully')



@receiver(post_save,sender=Cashier)
def create_new_portal_user(sender,instance,created,*args,**kwargs):
    if created:
        records = User.objects.get(email=instance.user)
        records.role_id=instance.role
        records.save()
        print('user role updated successfully')









