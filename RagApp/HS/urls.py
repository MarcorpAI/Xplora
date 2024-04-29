from django.urls import path
from . import views
from .views import QueryPDF, PDFView, XLXSView, QueryXLSX, DOCXView, QueryDocx

urlpatterns = [
    # Urls for .txt file uploads and querying(not really useful right now) work with the rest
    # path('file_interaction/', FileInteractionView.as_view(), name="file_upload_endpoint"),
    # path('query_view/', QueryView.as_view(), name="query_endpoint"),


    # # Urls for PDF upload and querying
    path('querypdf_view/', QueryPDF.as_view(), name='querypdf_view'),
    path('uploadpdf_view/', PDFView.as_view(), name="pdf_view"),
    
    # Urls for Excel files and querying
    path('uploadxlsx_view/', XLXSView.as_view(), name="xlsx_upload"),
    path('queryxlsx_view/', QueryXLSX.as_view(), name="xlsx_query"),


    path('uploaddocx_view/', DOCXView.as_view(), name="docx_upload"),
    path('querydocx_view/', QueryDocx.as_view(), name="docx_query"),



]
