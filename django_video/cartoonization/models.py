# Create your models here.
from django.db import models



class GetVideo(models.Model):
    video = models.FileField(upload_to='uploaded_video')