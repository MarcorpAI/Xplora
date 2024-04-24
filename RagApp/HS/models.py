from django.db import models
import uuid

# Create your models here.

class DocumentUpload(models.Model):
    file_name = models.CharField(max_length=100, blank=True)
    file_content = models.FileField(upload_to='uploads/')


    def __str__(self):
        return self.file_name
    

    

