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
 


"""
basically what every code does here is file upload and file query.....each file has a separate view the first view handles the file upload
and the second view handles the file interaction. when a file upload is successful...it fetches the query file endpoint where the user passes a prompt

""" 






class FileInteractionView(APIView):

    template_name = 'mainTXT.html'

    def get(self, request):
        return TemplateResponse(request, self.template_name)

    def post(self, request):
        print(request.POST)   # Check POST data
        print(request.FILES)  # Check uploaded files

        file_content = request.FILES.get('file_content')
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            file_path = document.file_content.path
            docs = data_ingestion_txt(file_path, encoding='utf-8')
            get_embeddings(docs)
            return Response({"document_id": document_id, "name": file_path})
            return TemplateResponse(request, self.template_name, {'document_id': document.id, 'name': file_path})
        else:
            print(form.errors)
            return Response({'error': 'Invalid form data'}, status=400)



class QueryView(APIView):
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.data.get('question')
        

        query = str(query)

        file_content = BytesIO(document.read())

        # Create an InMemoryUploadedFile object
        uploaded_file = InMemoryUploadedFile(
            file=file_content,
            field_name=None,
            name=document.name,
            content_type=document.content_type,
            size=document.size,
            charset=document.charset,
        )


        docs = data_ingestion_pdf(uploaded_file)
        vector_store = get_embeddings(docs)

        llm = get_openai_llm()
        answer = get_response_llm(llm, vector_store, query)

        return Response({"answer": answer})









class DocxView(APIView):

    template_name = 'index.html'

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










# query docx file
class QueryDocx(APIView):
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.data.get('question')

        query = str(query)

        # store the file in a temporary location
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            temp_file.write(document.read())
            temp_file_path = temp_file.name


        docs = data_ingestion_docx(temp_file_path)
        vector_store = get_embeddings(docs)

        llm = get_openai_llm()
        answer = get_response_llm(llm, vector_store, query)

        # remove the temporary file after processing
        os.unlink(temp_file_path)

        return Response({'answer': answer})












# this is the file upload for pdf
class PDFView(APIView):

    template_name = 'index.html'

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
            docs = data_ingestion_pdf(file_path)
            get_embeddings(docs)
            return TemplateResponse(request, self.template_name, {'document_id': document.id, 'name': file_path})
            
        else:
            print(form.errors)
            return Response({"error": 'invalid form data'}, status=400)







#query pdf files

class QueryPDF(APIView):
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.data.get('question')

        query = str(query)

        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            temp_file.write(document.read())
            temp_file_path = temp_file.name


        docs = data_ingestion_pdf(temp_file_path)
        vector_store = get_embeddings(docs)

        llm = get_openai_llm()
        answer = get_response_llm(llm, vector_store, query)

        # remove the temporary file after processing
        os.unlink(temp_file_path)
        return Response({'answer': answer})


 
 



#file upload for Excel file(loads it and stores it in a vector databse and prepares it for quering)
class XLXSView(APIView):

    template_name = 'index.html'

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




class QueryXLSX(APIView):
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.data.get('question')

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
            temp_file.write(document.read())
            temp_file_path = temp_file.name

        docs = data_ingestion_xlsx(temp_file_path)
        vector_store = get_embeddings(docs)

        llm = get_openai_llm()
        answer = get_response_llm(llm, vector_store, query)

        os.unlink(temp_file_path)

        return Response({"answer": answer})


        







