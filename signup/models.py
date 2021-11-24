from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    username = models.OneToOneField(User,on_delete = models.CASCADE, null=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return "{0} {1}".format(self.username,self.email_verified)
