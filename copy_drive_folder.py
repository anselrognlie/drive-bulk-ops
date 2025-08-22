import argparse
import sys
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google_auth_adapter import get_authenticated_drive

DEFAULT_PREFIX = "Copy of "

def copy_folder_recursively(drive, source_folder_id, destination_folder_id):
    """Recursively copies the contents of a source folder to a destination folder."""
    file_list = drive.ListFile({'q': f"'{source_folder_id}' in parents and trashed=false"}).GetList()

    for item in file_list:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            # Create a new subfolder in the destination folder
            new_subfolder = drive.CreateFile({
                'title': item['title'],
                'parents': [{'id': destination_folder_id}],
                'mimeType': 'application/vnd.google-apps.folder'
            })
            new_subfolder.Upload()
            print(f"Created folder: {item['title']}")
            # Recursively copy the contents of the subfolder
            copy_folder_recursively(drive, item['id'], new_subfolder['id'])
        else:
            # Create a PyDrive2 file object for the item
            file_to_copy = drive.CreateFile({'id': item['id']})
            file_to_copy.FetchMetadata(fields="title") # Fetch title for the new copy

            # Copy the file using PyDrive2's Copy() method
            # This creates a copy in the same parent folder as the original
            copied_file = file_to_copy.Copy(new_title=item['title']) # Keep original title

            # Update the parent of the copied file to the destination folder
            copied_file['parents'] = [{'id': destination_folder_id}]
            copied_file.Upload() # Apply changes (parent and title if changed)

            print(f"Copied file: {item['title']}")

def copy_drive_folder(drive: GoogleDrive, source_folder_id: str, new_folder_name: str | None = None):
    """Copies an entire Google Drive folder to a new folder in the same location."""
    try:
        # Get the source folder to find its parent
        source_folder = drive.CreateFile({'id': source_folder_id})
        source_folder.FetchMetadata(fields="parents, title")
        parent_id = source_folder['parents'][0]['id']

        # Calculate the new folder name if not supplied
        if not new_folder_name:
            new_folder_name = f"{DEFAULT_PREFIX}{source_folder['title']}"

        # print(f"Copying folder {source_folder['title']} to {new_folder_name}.")
        # return

        # Create the new folder in the same parent directory
        new_folder = drive.CreateFile({
            'title': new_folder_name,
            'parents': [{'id': parent_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        })
        new_folder.Upload()
        print(f"Created new folder: {new_folder_name}")

        # Recursively copy the contents
        copy_folder_recursively(drive, source_folder_id, new_folder['id'])

        print("\nFolder copy completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")



def main():
    parser = argparse.ArgumentParser(
        description="Recursively copy a Google Drive folder.",
        epilog="Example: python copy_drive_folder.py 123abcXYZ 'My Copied Folder'"
    )
    parser.add_argument("source_id", help="The ID of the source folder to copy.")
    parser.add_argument("dest_name", nargs='?', default=None, help=f'The name of the new destination folder. If omitted, "{DEFAULT_PREFIX}" will be prepended to the original folder name.')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    drive = get_authenticated_drive()

    # --- Instructions ---
    # 1. Make sure you have PyDrive2 installed: pip install PyDrive2
    # 2. Enable the Google Drive API and get your `client_secrets.json` file.
    #    (Follow the same steps as for the `rename_drive_files.py` script)
    # 3. Find the Google Drive folder ID of the folder you want to copy.
    copy_drive_folder(drive, args.source_id, args.dest_name)

if __name__ == "__main__":
    main()