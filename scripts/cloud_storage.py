"""
Google Cloud Storage integration for PhilAlignment.

This module provides functionality to upload response data to Google Cloud Storage.
"""

import os
import json
import datetime
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Google Cloud Storage configuration from environment variables
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
GCS_CREDENTIALS_PATH = os.getenv("GCS_CREDENTIALS_PATH")

# Set environment variable for Google Cloud credentials
if GCS_CREDENTIALS_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCS_CREDENTIALS_PATH

def is_cloud_storage_configured() -> bool:
    """
    Check if Google Cloud Storage is configured.
    
    Returns:
        True if Google Cloud Storage is configured, False otherwise
    """
    return bool(GCS_BUCKET_NAME and GCS_CREDENTIALS_PATH)

def upload_file_to_gcs(local_file_path: str, destination_blob_name: Optional[str] = None) -> bool:
    """
    Upload a file to Google Cloud Storage.
    
    Args:
        local_file_path: Path to the local file to upload
        destination_blob_name: Name of the blob in GCS (defaults to filename)
    
    Returns:
        True if upload was successful, False otherwise
    """
    if not is_cloud_storage_configured():
        print("Google Cloud Storage is not configured. Set GCS_BUCKET_NAME and GCS_CREDENTIALS_PATH in .env file.")
        return False
    
    if not os.path.exists(local_file_path):
        print(f"Error: File not found: {local_file_path}")
        return False
    
    try:
        from google.cloud import storage
        
        # If destination blob name is not provided, use the filename
        if not destination_blob_name:
            destination_blob_name = os.path.basename(local_file_path)
        
        # Initialize the client
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)
        
        # Upload the file
        blob.upload_from_filename(local_file_path)
        
        print(f"File {local_file_path} uploaded to gs://{GCS_BUCKET_NAME}/{destination_blob_name}")
        return True
    
    except ImportError:
        print("Error: Google Cloud Storage library not installed. Run 'pip install google-cloud-storage'")
        return False
    except Exception as e:
        print(f"Error uploading file to Google Cloud Storage: {str(e)}")
        return False

def upload_json_to_gcs(data: dict, destination_blob_name: str) -> bool:
    """
    Upload JSON data directly to Google Cloud Storage.
    
    Args:
        data: Dictionary to upload as JSON
        destination_blob_name: Name of the blob in GCS
    
    Returns:
        True if upload was successful, False otherwise
    """
    if not is_cloud_storage_configured():
        print("Google Cloud Storage is not configured. Set GCS_BUCKET_NAME and GCS_CREDENTIALS_PATH in .env file.")
        return False
    
    try:
        from google.cloud import storage
        
        # Initialize the client
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)
        
        # Convert data to JSON string
        json_data = json.dumps(data, indent=2)
        
        # Upload the JSON data
        blob.upload_from_string(json_data, content_type="application/json")
        
        print(f"JSON data uploaded to gs://{GCS_BUCKET_NAME}/{destination_blob_name}")
        return True
    
    except ImportError:
        print("Error: Google Cloud Storage library not installed. Run 'pip install google-cloud-storage'")
        return False
    except Exception as e:
        print(f"Error uploading JSON to Google Cloud Storage: {str(e)}")
        return False

def download_file_from_gcs(source_blob_name: str, destination_file_path: str) -> bool:
    """
    Download a file from Google Cloud Storage.
    
    Args:
        source_blob_name: Name of the blob in GCS
        destination_file_path: Path to save the downloaded file
    
    Returns:
        True if download was successful, False otherwise
    """
    if not is_cloud_storage_configured():
        print("Google Cloud Storage is not configured. Set GCS_BUCKET_NAME and GCS_CREDENTIALS_PATH in .env file.")
        return False
    
    try:
        from google.cloud import storage
        
        # Initialize the client
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(source_blob_name)
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
        
        # Download the file
        blob.download_to_filename(destination_file_path)
        
        print(f"File gs://{GCS_BUCKET_NAME}/{source_blob_name} downloaded to {destination_file_path}")
        return True
    
    except ImportError:
        print("Error: Google Cloud Storage library not installed. Run 'pip install google-cloud-storage'")
        return False
    except Exception as e:
        print(f"Error downloading file from Google Cloud Storage: {str(e)}")
        return False

def list_files_in_gcs(prefix: Optional[str] = None) -> list:
    """
    List files in Google Cloud Storage bucket.
    
    Args:
        prefix: Optional prefix to filter files
    
    Returns:
        List of file names in the bucket
    """
    if not is_cloud_storage_configured():
        print("Google Cloud Storage is not configured. Set GCS_BUCKET_NAME and GCS_CREDENTIALS_PATH in .env file.")
        return []
    
    try:
        from google.cloud import storage
        
        # Initialize the client
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        
        # List blobs
        blobs = bucket.list_blobs(prefix=prefix)
        
        # Return list of blob names
        return [blob.name for blob in blobs]
    
    except ImportError:
        print("Error: Google Cloud Storage library not installed. Run 'pip install google-cloud-storage'")
        return []
    except Exception as e:
        print(f"Error listing files in Google Cloud Storage: {str(e)}")
        return []

def backup_responses_to_gcs() -> bool:
    """
    Backup the responses file to Google Cloud Storage.
    
    Returns:
        True if backup was successful, False otherwise
    """
    import storage as local_storage
    
    # Ensure the storage file exists
    local_storage.ensure_storage_exists()
    
    # Create a timestamp for the backup
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destination_blob_name = f"backups/ai_responses_{timestamp}.json"
    
    # Upload the file
    return upload_file_to_gcs(local_storage.STORAGE_FILE, destination_blob_name)

def sync_responses_to_gcs() -> bool:
    """
    Sync the current responses file to Google Cloud Storage.
    This will overwrite the existing file in GCS.
    
    Returns:
        True if sync was successful, False otherwise
    """
    import storage as local_storage
    
    # Ensure the storage file exists
    local_storage.ensure_storage_exists()
    
    # Upload the file
    return upload_file_to_gcs(local_storage.STORAGE_FILE, "ai_responses.json")

def restore_responses_from_gcs(source_blob_name: Optional[str] = None) -> bool:
    """
    Restore responses from Google Cloud Storage.
    
    Args:
        source_blob_name: Name of the blob to restore (defaults to latest backup)
    
    Returns:
        True if restore was successful, False otherwise
    """
    import storage as local_storage
    
    # If source blob name is not provided, use the latest backup
    if not source_blob_name:
        backups = list_files_in_gcs("backups/")
        if not backups:
            print("No backups found in Google Cloud Storage.")
            return False
        
        # Sort backups by name (which includes timestamp)
        backups.sort()
        source_blob_name = backups[-1]
    
    # Download the file
    return download_file_from_gcs(source_blob_name, local_storage.STORAGE_FILE) 