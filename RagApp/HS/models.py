from django.db import models
import uuid
from django.contrib.auth import get_user_model
from allauth.account.signals import user_logged_in, user_signed_up
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import magic

file_validator = FileExtensionValidator(['docx', 'pdf', 'xlsx', 'txt', 'csv'])


User = get_user_model()




# code for file size limit 
def file_size_validator(value):  # value is the FileField instance
    filesize = value.size  # file size in bytes
    max_size = 1 * 1024 * 1024  # Define the maximum size as 5MB (adjust as needed)
    
    if filesize > max_size:
        raise ValidationError(f"File size exceeds the maximum allowed size of {max_size} bytes.")



#custom code to validate file mime types
def validate_file_mimetype(file):
    accept = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain', 'application/msword', 'application/vnd.ms-excel', 'text/csv']

    file_mime_type = magic.from_buffer(file.read(2024), mime=True)
    if file_mime_type not in accept:
        raise ValidationError("Unsupported file type")

class DocumentUpload(models.Model):
    file_name = models.CharField(max_length=100, blank=True)
    file_content = models.FileField(upload_to='uploads/', validators=[file_validator, validate_file_mimetype, file_size_validator])
    file_metadata = models.JSONField(blank=True, null=True)


    def __str__(self):
        if self.file_name:
            return self.file_name
        else:
            return f"Untitled Document ({self.pk})"




def user_signed_up_receiver(request, user, **kwargs):
    print(request)
    print(user)

user_signed_up.connect(user_signed_up_receiver, sender=User)


def user_logged_in_receiver(request, user, **kwargs):
    print(request)
    print(user)

user_logged_in.connect(user_logged_in_receiver, sender=User)

    


    

