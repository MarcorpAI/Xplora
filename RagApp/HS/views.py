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

 




class FileInteractionView(APIView):

    template_name = 'main1.html'

    def get(self, request):
        return TemplateResponse(request, self.template_name)

    @csrf_exempt
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

    template_name = 'main1.html'

    def get(self, request):
        return TemplateResponse(request, self.template_name)


    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.data.get('question')
        

        query = str(query)

        # Save the uploaded file to a temporary location on disk
        fs = FileSystemStorage()
        temp_file_path = fs.save(document.name, document)

        # Pass the temporary file path to the data_ingestion_txt function
        docs = data_ingestion_txt(temp_file_path, encoding='utf-8')
        vector_store = get_embeddings(docs)

        llm = get_openai_llm()
        answer = get_response_llm(llm, vector_store, query)

        return Response({"answer": answer})







class DocxView(APIView):

    template_name = 'main1.html'

    def get(self, request):
        return TemplateResponse(request, self.template_name)

    @csrf_exempt
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

        # Save the uploaded file to a temporary location on disk
        fs = FileSystemStorage()
        temp_file_path = fs.save(document.name, document)

        # Pass the temporary file path to the data_ingestion_txt function
        docs = data_ingestion_docx(temp_file_path)
        vector_store = get_embeddings(docs)

        llm = get_openai_llm()
        answer = get_response_llm(llm, vector_store, query)

        # Remove the temporary file
        os.remove(temp_file_path)

        return Response({'answer': answer})




# this is the file upload for pdf
class PDFView(APIView):
    @csrf_exempt
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
            return Response({"document_id": document.id, "name": file_path})
        else:
            print(form.errors)
            return Response({"error": 'invalid form data'}, status=400)










#query pdf files

class QueryPDF(APIView):
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.data.get('question')

        query = str(query)

        # Save the uploaded file to a temporary location on disk
        fs = FileSystemStorage()
        temp_file_path = fs.save(document.name, document)

        # Pass the temporary file path to the data_ingestion_txt function
        docs = data_ingestion_pdf(temp_file_path)
        vector_store = get_embeddings(docs)

        llm = get_openai_llm()
        answer = get_response_llm(llm, vector_store, query)

        # Remove the temporary file
        os.remove(temp_file_path)

        return Response({'answer': answer})


 
# query excel files files




class XLXSView(APIView):

    template_name = 'main1.html'

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













# class QueryXLSX(APIView):
#     def post(self, request):
#         document = request.FILES.get('file_content')
#         query = request.data.get('question')
#         file_name = request.FILES.get("file_name")

#         query = str(query)

#         # Save the uploaded file to a temporary location on disk
#         fs = FileSystemStorage()
#         temp_file_path = fs.save(document.file_name, document)

#         # Pass the temporary file path to the data_ingestion_txt function
#         docs = data_ingestion_xlsx(temp_file_path)
#         vector_store = get_embeddings(docs)

#         llm = get_openai_llm()
#         answer = get_response_llm(llm, vector_store, query)

#         # Remove the temporary file
#         os.remove(temp_file_path)

#         return Response({'answer': answer})


class QueryXLSX(APIView):
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.data.get('question')

        if not document:
            return Response({'error': 'No file uploaded'}, status=400)
            print(Response)

        query = str(query)

        try:
            # Save the uploaded file to a temporary location on disk
            fs = FileSystemStorage()
            temp_file_path = fs.save(document.name, document)

            # Pass the temporary file path to the data_ingestion_xlsx function
            docs = data_ingestion_xlsx(temp_file_path)
            vector_store = get_embeddings(docs)

            llm = get_openai_llm()
            answer = get_response_llm(llm, vector_store, query)

            # Remove the temporary file
            os.remove(temp_file_path)

            return Response({'answer': answer})

        except Exception as e:
            # Handle any exceptions that might occur during file processing
            return Response({'error': str(e)}, status=500)







