import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .service import AzureAIService, AzureMLService
import os
import base64

# Constants
from .constants import *

@api_view(['GET'])
def health(request):
    try:
        return JsonResponse({'status': 'Service is healthy'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['POST'])
def chat(request):
    try:
        data = request.data
        azure_service = AzureAIService()
        result = azure_service.chat(data)
        return JsonResponse(json.loads(result), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
def upload_files(request):
    try:
        files = request.data.get('files')
        
        if not files or not isinstance(files, list):
            return JsonResponse({'error': 'Files should be a list of objects containing file name and file data.'}, status=400)
        
        file_data_list = []
        for file_obj in files:
            file_name = file_obj.get('name')
            file_content_base64 = file_obj.get('file')
            
            if not file_name or not file_content_base64:
                return JsonResponse({'error': 'Each file object must contain a name and file data.'}, status=400)
            
            file_content = base64.b64decode(file_content_base64)
            file_data_list.append({'name': file_name, 'content': file_content})
        
        azure_service = AzureMLService()
        azure_service.update_index(file_data_list)
        
        return JsonResponse({'message': 'Files uploaded and indexed successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
