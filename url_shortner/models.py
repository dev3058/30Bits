from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class UrlLead(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    redirect_path = models.URLField(blank=False,default='https://3058.in')
    shortened_url = models.SlugField(unique=True, db_index=True, default='/', validators=[MinLengthValidator(5),MaxLengthValidator(20)])
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    def __str__(self):
        return self.shortened_url

class ImageStorage(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,related_name="image_user")
    image = models.ImageField(upload_to = "images")
    

    