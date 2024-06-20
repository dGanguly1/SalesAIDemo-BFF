import os
import ssl
import json
import shutil
import urllib.request
from .constants import *
# from azure.identity import DefaultAzureCredential 
# from azure.ai.ml import MLClient
# from azure.ai.ml.entities import IndexModelConfiguration, AzureAISearchConfig
# from azure.core.exceptions import ResourceNotFoundError


def allowSelfSignedHttps(allowed): 
    # Bypass the server certificate verification on the client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

class AzureAIService:
    def __init__(self):
        allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

    def chat(self, data):
        body = str.encode(json.dumps(data))

        url = AZURE_BASE_ADDRESS
        api_key = AZURE_API_KEY

        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'azureml-model-deployment': AZURE_MODEL_DEPLOYMENT
        }
        req = urllib.request.Request(url, data=body, headers=headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            print(result)
            return result
        except urllib.error.HTTPError as error:
            error_info = {
                "status_code": error.code,
                "headers": dict(error.headers),
                "body": error.read().decode("utf8", 'ignore')
            }
            return json.dumps(error_info)


# class AzureMLService:
#     def __init__(self):
#         self.client = MLClient(
#             DefaultAzureCredential(),
#             subscription_id=SUBSCRIPTION_ID,
#             resource_group_name=RESOURCE_GROUP_NAME,
#             workspace_name=AZURE_WORKSPACE_NAME
#         )
    
#     def get_ai_search_connection(self):
#         return self.client.connections.get(AZURE_SEARCH_CONNECTION_NAME)

#     def get_embeddings_model_config(self):
#         aoai_connection = self.client.connections.get(AZURE_API_KEY, populate_secrets=True)
#         return IndexModelConfiguration.from_connection(
#             aoai_connection, 
#             model_name="text-embedding-ada-002", 
#             deployment_name="text-embedding-ada-002"
#         )

#     def delete_existing_index_data(self, INDEX_NAME):
#         try:
#             index_client = self.client.search.get_index_client()
#             index_client.delete_documents(INDEX_NAME);.
#         except ResourceNotFoundError:
#             pass

#     def write_files_to_local(self, file_data_list):
#         temp_dir = os.path.join(os.getenv('TEMP_DIR', '/tmp'), 'upload_files')
#         if not os.path.exists(temp_dir):
#             os.makedirs(temp_dir)
        
#         file_paths = []
#         for file_data in file_data_list:
#             file_name = file_data['name']
#             file_content = file_data['content']
#             file_path = os.path.join(temp_dir, file_name)
#             with open(file_path, 'wb') as file:
#                 file.write(file_content)
#             file_paths.append(file_path)
        
#         return file_paths

#     def cleanup_local_files(self, file_paths):
#         temp_dir = os.path.dirname(file_paths[0])
#         for file_path in file_paths:
#             os.remove(file_path)
#         shutil.rmtree(temp_dir)

#     def upload_files_to_index(self, file_data_list):
#         ai_search_connection = self.get_ai_search_connection()
#         embeddings_model_config = self.get_embeddings_model_config()
        
#         file_paths = self.write_files_to_local(file_data_list)
        
#         from azure.ai.ml.entities import LocalSource
#         input_source = LocalSource(input_data=file_paths)
        
#         try:
#             self.client.indexes.build_index(
#                 name=INDEX_NAME,
#                 embeddings_model_config=embeddings_model_config,
#                 input_source=input_source,
#                 index_config=AzureAISearchConfig(
#                     ai_search_index_name=INDEX_NAME,
#                     ai_search_connection_id=ai_search_connection.id
#                 ),
#                 tokens_per_chunk=800,
#                 token_overlap_across_chunks=0,
#             )
#         finally:
#             self.cleanup_local_files(file_paths)
        
#     def update_index(self, file_data_list):
#         self.delete_existing_index_data()
#         self.upload_files_to_index(file_data_list)

