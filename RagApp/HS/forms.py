from django import forms
from .models import DocumentUpload

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ["file_content"]  # Adjust fields if needed


class QuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea)



class DatabaseConnectionForm(forms.Form):
    user = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    host = forms.CharField(max_length=100)
    port = forms.CharField(max_length=5)
    database = forms.CharField(max_length=100)



class UserQueryForm(forms.Form):
    question = forms.CharField(max_length=255)