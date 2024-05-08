from django.db import models
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import magic

file_validator = FileExtensionValidator(['docx', 'pdf', 'xlsx', 'txt'])


#custom code to validate file mime types
def validate_file_mimetype(file):
    accept = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain', 'application/msword', 'application/vnd.ms-excel']

    file_mime_type = magic.from_buffer(file.read(2024), mime=True)
    if file_mime_type not in accept:
        raise ValidationError("Unsupported file type")

class DocumentUpload(models.Model):
    file_name = models.CharField(max_length=100, blank=True)
    file_content = models.FileField(upload_to='uploads/', validators=[file_validator, validate_file_mimetype])
    file_metadata = models.JSONField(blank=True, null=True)


    def __str__(self):
        if self.file_name:
            return self.file_name
        else:
            return f"Untitled Document ({self.pk})"
    

    

