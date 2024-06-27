import os



project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ragapp_dir = os.path.join(project_root, 'RagApp')
sys.path.append(project_root)
sys.path.append(ragapp_dir)
settings_module = 'RagApp.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'RagApp.settings'

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
