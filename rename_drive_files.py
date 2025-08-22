from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google_auth_adapter import get_authenticated_drive

def rename_files_in_folder(drive: GoogleDrive, folder_id: str):
    """
    Renames files in a specified Google Drive folder that begin with "Copy of ".

    Args:
        drive: The authenticated GoogleDrive instance.
        folder_id: The ID of the Google Drive folder.
    """
    try:
        # List all files in the specified folder.
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

        for file_item in file_list:
            if file_item['title'].startswith("Copy of "):
                original_title = file_item['title']
                new_title = original_title.replace("Copy of ", "", 1)
                print(f"Renaming '{original_title}' to '{new_title}'...")
                file_item['title'] = new_title
                file_item.Upload()
                print(f"Successfully renamed to '{new_title}'.")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # --- Instructions ---
    # 1. Make sure you have PyDrive2 installed: pip install PyDrive2
    # 2. Enable the Google Drive API and get your `client_secrets.json` file.
    #    - Go to https://console.developers.google.com/
    #    - Create a new project.
    #    - Enable the "Google Drive API".
    #    - Create credentials for a "Desktop app".
    #    - Download the credentials as `client_secrets.json` and place it in the
    #      same directory as this script.
    # 3. Find the Google Drive folder ID.
    #    - Open the folder in your web browser.
    #    - The folder ID is the last part of the URL.
    #      (e.g., in https://drive.google.com/drive/folders/12345abcdef, the ID is "12345abcdef")
    # 4. Replace "YOUR_FOLDER_ID" with your actual folder ID.

    # Replace "YOUR_FOLDER_ID" with the ID of your Google Drive folder.
    TARGET_FOLDER_ID = "1pvwOfyMSAYQvxAvsLbE5jyupWn39tQRa"

    if TARGET_FOLDER_ID == "YOUR_FOLDER_ID":
        print("Please replace 'YOUR_FOLDER_ID' with your actual Google Drive folder ID in the script.")
    else:
        drive = get_authenticated_drive()
        rename_files_in_folder(drive, TARGET_FOLDER_ID)

if __name__ == "__main__":
    main()
