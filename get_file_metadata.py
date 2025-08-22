from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google_auth_adapter import get_authenticated_drive

def get_file_metadata(file_id):
    drive = get_authenticated_drive()
    try:
        file_item = drive.CreateFile({'id': file_id})
        file_item.FetchMetadata()
        print(f"File Title: {file_item['title']}")
        print(f"File ID: {file_item['id']}")
        print(f"MIME Type: {file_item['mimeType']}")
        print(f"Parents: {file_item['parents']}")
        print(f"Trashed: {file_item['labels']['trashed']}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace with the problematic file ID
    PROBLEM_FILE_ID = '1B-fFnur4jKOelHnQ3zxNNMCNLaLHzTtE0JOddgEPX14'
    get_file_metadata(PROBLEM_FILE_ID)
