from django.conf import settings
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token_on_user_create(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#test model for transaction example
class Place(models.Model):
    name = models.CharField(max_length=20)
    street = models.CharField(max_length=50)
    street_number = models.IntegerField()
    office = models.IntegerField()
    change = models.BooleanField(default=False)

    def set_office(self):
        with transaction.atomic():
            self.office = 15
            self.save()
            transaction.on_commit(self.set_change_status)

    def set_change_status(self):
        self.change = True
        self.save()
