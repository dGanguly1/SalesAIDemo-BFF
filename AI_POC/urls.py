from django.urls import path
from .views import chat, health, upload_files

urlpatterns = [
    path('health', health),
    path('chat', chat),
    path('upload-files', upload_files),
]
