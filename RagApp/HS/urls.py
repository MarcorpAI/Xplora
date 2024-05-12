from django.urls import path
from . import views
from .views import QueryPDF, PDFView, XLSXView, QueryXLSX, DOCXView, QueryDocx, CSVView, QueryCSV
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),

    # # Urls for PDF upload and querying
    path('querypdf_view/', QueryPDF.as_view(), name='querypdf_view'),
    path('', PDFView.as_view(), name="pdf_view"),


    path('querycsv_view/', QueryCSV.as_view(), name='querycsv_view'),
    path('uploadcsv_view/', CSVView.as_view(), name="csv_view"),
    
    # Urls for Excel files and querying
    path('uploadxlsx_view/', XLSXView.as_view(), name="xlsx_upload"),
    path('queryxlsx_view/', QueryXLSX.as_view(), name="xlsx_query"),


    path('uploaddocx_view/', DOCXView.as_view(), name="docx_upload"),
    path('querydocx_view/', QueryDocx.as_view(), name="docx_query"),



]
