from django.urls import path
from .views import chat, health#, upload_files

urlpatterns = [
    path('chat/', chat),
    path('health', health),
    # path('upload-files/', upload_files),
]
