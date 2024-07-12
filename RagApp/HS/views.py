from django.shortcuts import render 
from django.shortcuts import render, redirect
from .forms import DocumentUploadForm , QuestionForm,  DatabaseConnectionForm, UserQueryForm
from .models import DocumentUpload
from.llm import data_ingestion_txt, get_embeddings, get_openai_llm, get_response_llm, data_ingestion_docx, data_ingestion_pdf,data_ingestion_xlsx, data_ingestion_csv, format_answer
from django.contrib import messages
from django.views.decorators.http import require_http_methods 
from django.views.decorators.csrf import csrf_exempt 
from .sql_engine import init_database, get_sql_chain, get_response, init_database_postgres
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
from rest_framework import status
from django.http import HttpResponse
from django.contrib import messages
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

 


"""
basically what every code does here is file upload and file query.....each file has a separate view the first view handles the file upload
and the second view handles the file interaction. when a file upload is successful...it fetches the query file endpoint where the user passes a prompt

""" 

 

# index page view - added this index page
class IndexView(APIView):
    template_name = 'HS/index.html'
    redirect_field_name = 'next'

    def get(self, request):
        return TemplateResponse(request, self.template_name)











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






# Utility function to determine file type and call the appropriate ingestion function
def ingest_file(file_path, file_extension):
    if file_extension == '.pdf':
        return data_ingestion_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        return data_ingestion_docx(file_path)
    elif file_extension in ['.xlsx', '.xls']:
        return data_ingestion_xlsx(file_path)
    elif file_extension == '.csv':
        return data_ingestion_csv(file_path)
    else:
        raise ValueError("Unsupported file format")









class UploadView(LoginRequiredMixin, APIView):
    template_name = 'HS/excel1.html'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            file_path = document.file_content.path
            file_extension = os.path.splitext(file_path)[1].lower()

            try:
                docs = ingest_file(file_path, file_extension)
                get_embeddings(docs)
                return render(request, self.template_name, {'document_id': document.id, 'name': file_path})
            except ValueError as e:
                logger.error(e)
                return Response({"error": str(e)}, status=400)
        else:
            logger.error(form.errors)
            return Response({"error": 'invalid form data'}, status=400)



class QueryFile(APIView):
    # @method_decorator(require_POST)
    def post(self, request):
        document = request.FILES.get('file_content')
        query = request.POST.get('question')
        if not document or not query:
            return Response({'error': 'file_content and question are required.'}, status=400)

        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(document.name)[1]) as temp_file:
            for chunk in document.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            file_extension = os.path.splitext(temp_file_path)[1].lower()
            docs = ingest_file(temp_file_path, file_extension)

            metadata_filter = {}

            vector_store = get_embeddings(docs)
            llm = get_openai_llm()
            answer = get_response_llm(llm, vector_store, query, os.path.basename(temp_file_path), metadata_filter)

            os.remove(temp_file_path)
            return JsonResponse({'answer': answer})
        except Exception as e:
            logger.error(e)
            os.remove(temp_file_path)
            return Response({'error': str(e)}, status=500)







class DatabaseConnectionView(LoginRequiredMixin,APIView):
    redirect_field_name = 'next'
    template_name = 'HS/connect_database.html'


    def get(self, request):
        database_form = DatabaseConnectionForm()
        return render(request, 'HS/connect_database.html', {'database_form': database_form})

    def post(self, request):
        database_form = DatabaseConnectionForm(request.POST)
        if database_form.is_valid():
            user = database_form.cleaned_data['user']
            password = database_form.cleaned_data['password']
            host = database_form.cleaned_data['host']
            port = database_form.cleaned_data['port']
            database = database_form.cleaned_data['database']

            try:
                # Store connection parameters in the session
                request.session['db_params'] = {
                    'user': user,
                    'password': password,
                    'host': host,
                    'port': port,
                    'database': database
                }
                # Inform user about successful connection
                
                db = init_database(user, password, host, port, database)
                return Response({'status': 'success', 'message': 'Connection Successful!'})
                message.success(request, "successful")
            except Exception as e:
                # Handle connection initialization error
                messages.warning(request, f"Connection Failed! Error: {e}")
                return Response({'status': 'error', 'message': f'Database connection failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'status': 'error', 'message': 'Invalid form data.'}, status=status.HTTP_400_BAD_REQUEST)


class QueryDatabaseView(APIView):
    def post(self, request):
        query_form = UserQueryForm(request.POST)
        if query_form.is_valid():
            question = query_form.cleaned_data['question']
            # Retrieve connection parameters from the session
            db_params = request.session.get('db_params')
            if db_params:
                try:
                    # Recreate the SQLDatabase object from session parameters
                    db = init_database(**db_params)

                    chat_history = cache.get(f'chat_history_{request.user.id}', [])
                    chat_history = chat_history[-5:]
                    answer = get_response(question, db, chat_history)

                    chat_history.append((question, answer))
                    cache.set(f'chat_history_{request.user.id}', chat_history, timeout=3600)

                    return Response({'status': 'success', 'response': answer})
                except Exception as e:
                    return Response({'status': 'error', 'message': f'Error executing query: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'status': 'error', 'message': 'No active database connection.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error', 'message': 'Invalid form data.'}, status=status.HTTP_400_BAD_REQUEST)















class PostgreSQLView(LoginRequiredMixin,APIView):
    redirect_field_name = 'next'
    template_name = 'HS/postgres.html'


    def get(self, request):
        database_form = DatabaseConnectionForm()
        return render(request, 'HS/postgres.html', {'database_form': database_form})

    def post(self, request):
        database_form = DatabaseConnectionForm(request.POST)
        if database_form.is_valid():
            user = database_form.cleaned_data['user']
            password = database_form.cleaned_data['password']
            host = database_form.cleaned_data['host']
            port = database_form.cleaned_data['port']
            database = database_form.cleaned_data['database']

            try:
                # Store connection parameters in the session
                request.session['db_params'] = {
                    'user': user,
                    'password': password,
                    'host': host,
                    'port': port,
                    'database': database
                }
                # Inform user about successful connection

                return Response({'status': 'success', 'message': 'Connection Successful!'})
                message.success(request, "successful")
            except Exception as e:
                # Handle connection initialization error
                messages.warning(request, f"Connection Failed! Error: {e}")
                return Response({'status': 'error', 'message': f'Database connection failed: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'status': 'error', 'message': 'Invalid form data.'}, status=status.HTTP_400_BAD_REQUEST)


class QueryPostgres(APIView):
    def post(self, request):
        query_form = UserQueryForm(request.POST)
        if query_form.is_valid():
            question = query_form.cleaned_data['question']
            # Retrieve connection parameters from the session
            db_params = request.session.get('db_params')
            if db_params:
                try:
                    # Recreate the SQLDatabase object from session parameters
                    db = init_database_postgres(**db_params)

                    chat_history = request.session.get('chat_history', [])
                    chat_history = chat_history[-5:]
                    answer = get_response(question, db, chat_history)

                    chat_history.append((question, answer))

                    request.session['chat_history'] = chat_history
                    return Response({'status': 'success', 'response': answer})
                except Exception as e:
                    return Response({'status': 'error', 'message': f'Error executing query: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'status': 'error', 'message': 'No active database connection.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error', 'message': 'Invalid form data.'}, status=status.HTTP_400_BAD_REQUEST)


def docs_view(request):
    return render(request, "HS/docs.html", {})