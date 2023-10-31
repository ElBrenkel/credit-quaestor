import os
import pathlib

import dropbox
from dotenv import load_dotenv
from dropbox.exceptions import AuthError

load_dotenv()
DROPBOX_TOKEN = os.environ.get("DROPBOX_TOKEN")


def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def dropbox_upload_file(local_path, local_file, dropbox_file_path):
    """Upload a file from the local machine to a path in the Dropbox app directory.

    Args:
        local_path (str): The path to the local file.
        local_file (str): The name of the local file.
        dropbox_file_path (str): The path to the file in the Dropbox app directory.

    Example:
        dropbox_upload_file('.', 'test.csv', '/stuff/test.csv')

    Returns:
        meta: The Dropbox file metadata.
    """
    try:
        dbx = dropbox_connect()
        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))
            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))


if __name__ == "__main__":
    dropbox_upload_file("C:\\Users\\Elad\\Downloads", "Untitled.jpg", "/test/pic.jpg")
