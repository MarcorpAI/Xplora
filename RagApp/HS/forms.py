from django import forms
from .models import DocumentUpload

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ["file_name","file_content"]  # Adjust fields if needed


class QuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea)

