from django.shortcuts import render 
from django.shortcuts import render, redirect
from .forms import DocumentUploadForm , QuestionForm
from .models import DocumentUpload
from.llm import data_ingestion_txt, get_embeddings, get_openai_llm, get_response_llm, data_ingestion_docx, data_ingestion_pdf, data_ingestion_xlsx
from django.contrib import messages
from django.views.decorators.http import require_http_methods 
from django.views.decorators.csrf import csrf_exempt 

from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError, HttpResponseNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import json
import os
from django.core.files.storage import FileSystemStorage
from django.template.response import TemplateResponse
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import tempfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser
import hashlib
 


"""
basically what every code does here is file upload and file query.....each file has a separate view the first view handles the file upload
and the second view handles the file interaction. when a file upload is successful...it fetches the query file endpoint where the user passes a prompt

""" 





# class FileInteractionView(APIView):

#     template_name = 'mainTXT.html'

#     def get(self, request):
#         return TemplateResponse(request, self.template_name)

#     def post(self, request):
#         print(request.POST)   # Check POST data
#         print(request.FILES)  # Check uploaded files

#         file_content = request.FILES.get('file_content')
#         form = DocumentUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             document = form.save()
#             file_path = document.file_content.path
#             docs = data_ingestion_txt(file_path, encoding='utf-8')
#             get_embeddings(docs)
#             return Response({"document_id": document_id, "name": file_path})
#             return TemplateResponse(request, self.template_name, {'document_id': document.id, 'name': file_path})
#         else:
#             print(form.errors)
#             return Response({'error': 'Invalid form data'}, status=400)



# class QueryView(APIView):
#     def post(self, request):
#         document = request.FILES.get('file_content')
#         query = request.data.get('question')
        

#         query = str(query)

#         file_content = BytesIO(document.read())

#         # Create an InMemoryUploadedFile object
#         uploaded_file = InMemoryUploadedFile(
#             file=file_content,
#             field_name=None,
#             name=document.name,
#             content_type=document.content_type,
#             size=document.size,
#             charset=document.charset,
#         )


#         docs = data_ingestion_pdf(uploaded_file)
#         vector_store = get_embeddings(docs)

#         llm = get_openai_llm()
#         answer = get_response_llm(llm, vector_store, query)

#         return Response({"answer": answer})






# code for txt file above (dont bother about that one)


def hash_file(file_path):
    """
    Calculate the hash of a file's content.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The SHA-256 hash of the file content.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update the hash in chunks
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()













# view function that handles file uploads for PDF files

# @method_decorator(login_required, name='dispatch')
class PDFView(LoginRequiredMixin,APIView):
    template_name = 'work.html'
    redirect_field_name = 'next'
    


    # @method_decorator(login_required)
    def get(self, request):
        return TemplateResponse(request, self.template_name)

    # @method_decorator(login_required)
    def post(self, request):
        print(request.POST)
        print(request.FILES)

        file_content = request.FILES.get("file_content")
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            file_path = document.file_content.path
            docs = data_ingestion_pdf(file_path)
            get_embeddings(docs)
            return TemplateResponse(request, self.template_name, {'document_id': document.id, 'name': file_path})
            
        else:
            print(form.errors)
            return Response({"error": 'invalid form data'}, status=400)

 

# view function that handles file querying for PDF files

class QueryPDF(APIView):
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.POST.get('question')
        if not document or not query:
            return Response({'error': 'file_content and question are required.'}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            for chunk in document.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            docs = data_ingestion_pdf(temp_file_path)

            # Apply a metadata filter if needed
            metadata_filter = {}  # Example: Adjust or remove as necessary

            vector_store = get_embeddings(docs, metadata_filter)

            llm = get_openai_llm()
            answer = get_response_llm(llm, vector_store, query, os.path.basename(temp_file_path), metadata_filter)

            # Clean up the temporary file
            os.remove(temp_file_path)

            return Response({'answer': answer})
        except Exception as e:
            # Clean up and respond with error
            os.remove(temp_file_path)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












# view function that handles file upload for excel files

class XLSXView(LoginRequiredMixin, APIView):

    template_name = 'excel1.html'
    redirect_field_name = 'next'


    def get(self, request):
        return TemplateResponse(request, self.template_name)

    def post(self, request):
        print(request.POST)
        print(request.FILES)

        file_content = request.FILES.get("file_content")
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            file_path = document.file_content.path
            docs = data_ingestion_xlsx(file_path)
            get_embeddings(docs)
            return TemplateResponse(request, self.template_name, {'document_id': document.id, 'name': file_path})
            
        else:
            print(form.errors)
            return Response({"error": 'invalid form data'}, status=400)



# view that handles querying excel files
class QueryXLSX(APIView):
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.POST.get('question')
        if not document or not query:
            return Response({'error': 'file_content and question are required.'}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            for chunk in document.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            docs = data_ingestion_xlsx(temp_file_path)

            # Apply a metadata filter if needed
            metadata_filter = {}  # Example: Adjust or remove as necessary

            vector_store = get_embeddings(docs, metadata_filter)

            llm = get_openai_llm()
            answer = get_response_llm(llm, vector_store, query, os.path.basename(temp_file_path), metadata_filter)

            # Clean up the temporary file
            os.remove(temp_file_path)

            return Response({'answer': answer})
        except Exception as e:
            # Clean up and respond with error
            os.remove(temp_file_path)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#view than handles file upload for docx files 

class DOCXView(LoginRequiredMixin, APIView):

    template_name = 'docx.html'
    redirect_field_name = 'next'


    def get(self, request):
        return TemplateResponse(request, self.template_name)

    def post(self, request):
        print(request.POST)
        print(request.FILES)

        file_content = request.FILES.get("file_content")
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            file_path = document.file_content.path
            docs = data_ingestion_docx(file_path)
            get_embeddings(docs)
            return TemplateResponse(request, self.template_name, {'document_id': document.id, 'name': file_path})
            
        else:
            print(form.errors)
            return Response({"error": 'invalid form data'}, status=400)

        

# view that handles querying of docx files
class QueryDocx(APIView):
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.POST.get('question')
        if not document or not query:
            return Response({'error': 'file_content and question are required.'}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
            for chunk in document.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            docs = data_ingestion_docx(temp_file_path)

            # Apply a metadata filter if needed
            metadata_filter = {}  # Example: Adjust or remove as necessary

            vector_store = get_embeddings(docs, metadata_filter)

            llm = get_openai_llm()
            answer = get_response_llm(llm, vector_store, query, os.path.basename(temp_file_path), metadata_filter)

            # Clean up the temporary file
            os.remove(temp_file_path)

            return Response({'answer': answer})
        except Exception as e:
            # Clean up and respond with error
            os.remove(temp_file_path)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








