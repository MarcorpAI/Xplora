from django.urls import path
from . import views
from .views import QueryFile, UploadView, DatabaseConnectionView, QueryDatabaseView, IndexView, PostgreSQLView, QueryPostgres
from django.contrib.auth import views as auth_views

urlpatterns = [
    # index page
    path('', IndexView.as_view(), name='index'),
    
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),

    # # Urls for PDF upload and querying
    path('queryfile_view/', QueryFile.as_view(), name='queryfile_view'),
    path('chatwfile/', UploadView.as_view(), name="uploadfile_view"),
    
    # # Urls for Excel files and querying
 

    path('askdatabase/', DatabaseConnectionView.as_view(), name='db_connect'),
    path('query/', QueryDatabaseView.as_view(), name='db_query'),

    path('askpostgres/', PostgreSQLView.as_view(), name='db_postgres'),
    path('querypost/', QueryPostgres.as_view(), name='post_query'),


    # path('query/', QueryDBView.as_view(), name='db_query'),



]
