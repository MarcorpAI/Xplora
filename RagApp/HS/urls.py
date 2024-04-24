from django.urls import path
from . import views
from.views import FileInteractionView, QueryView, DocxView, QueryDocx, QueryPDF, PDFView, XLXSView, QueryXLSX

urlpatterns = [
    path('file_interaction/', FileInteractionView.as_view(), name="file_upload_endpoint"),
    path('query_view/', QueryView.as_view(), name="query_endpoint"),
    path('uploaddocx_view/', DocxView.as_view(), name='docx_upload'),
    path('uploadpdf_view/', PDFView.as_view(), name="docx_query"),
    
    path('uploadxlsx_view/', XLXSView.as_view(), name="xlsx_upload"),
    path('queryxlsx_view/', QueryXLSX.as_view(), name="xlsx_query"),



    path('querydocx_view/', QueryDocx.as_view()),
    path('querypdf_view/', QueryPDF.as_view()),


]

# urlpatterns = [
#     # path('index/', views.index, name='index'),
#     path('file_interaction/', views.file_interaction_view, name='file_interaction'),
#     path("query/", views.query_view, name="query_view")
#     # path('task/<uuid:task_id>/', views.task_status, name='task_status'),


#     # Add other URL patterns as needed
# ]
