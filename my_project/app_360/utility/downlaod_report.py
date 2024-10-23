from django.http import HttpResponse
from azure.storage.blob import BlobServiceClient

from django.conf import settings


# Configure your Azure Storage connection
AZURE_CONNECTION_STRING = settings.AZURE_CONNECTION_STRING 

def download_pdf(request, name, participant_id):
    #company_id = int(request.COOKIES.get('company_id'))
    company_id = 2
    
    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_name = f'company-{company_id}'
    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)
    try:
        # Get the blob client for the specific PDF file
        blob_client = container_client.get_blob_client(str(name) + '_' + str(participant_id) + '_executive_summary.pdf')

        # Download the blob (PDF file)
        stream = blob_client.download_blob()

        # Prepare the response
        response = HttpResponse(stream.readall(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{name}_{participant_id}_executive_summary.pdf"'
        
        return response
    
    except Exception as e:
        # Handle exceptions (e.g., file not found)
        return HttpResponse(f"Error: {str(e)}", status=404)
