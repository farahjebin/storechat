import os
import datetime
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

# Scope changed to full Drive access to see shared files  
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Replace with your actual credentials file
FILE_NAME = 'chat_history'
FOLDER_ID = 'YOUR_FOLDER_ID_HERE'  # Replace with your Google Drive folder ID

class GoogleDriveStorage:
    def __init__(self):
        self.creds = None
        self.file_id = None
        self.file_type = None  # 'text' or 'doc'
        self.file_id_path = "google_drive_file_id.txt"
        self._authenticate()
        self._find_file()

    def _authenticate(self):
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            self.creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        else:
            raise FileNotFoundError(f"Service account file '{SERVICE_ACCOUNT_FILE}' not found.")

    def _find_file(self):
        # build the Drive v3 service
        service = build('drive', 'v3', credentials=self.creds)

        # Search for the file by name INSIDE the shared folder (either .txt or Google Doc)
        query = f"name contains '{FILE_NAME}' and '{FOLDER_ID}' in parents and trashed = false"
        results = service.files().list(q=query, spaces='drive', fields='files(id, name, mimeType)').execute()
        items = results.get('files', [])

        if not items:
            raise FileNotFoundError(f"No file matching '{FILE_NAME}' found in the shared folder. Please create one manually.")

        # Prefer the user-created file (usually the Google Doc or .txt without service account ownership)
        for item in items:
            mime = item['mimeType']
            if mime == 'application/vnd.google-apps.document':
                self.file_id = item['id']
                self.file_type = 'doc'
                print(f"Found Google Doc: {item['name']} (ID: {self.file_id})")
                return
            elif mime == 'text/plain':
                self.file_id = item['id']
                self.file_type = 'text'
                print(f"Found text file: {item['name']} (ID: {self.file_id})")
                return

        # Fallback: use first item
        self.file_id = items[0]['id']
        self.file_type = 'unknown'
        print(f"Using file: {items[0]['name']} (ID: {self.file_id}, Type: {items[0]['mimeType']})")

    def append_chat_log(self, question: str, answer: str):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if self.file_type == 'doc':
                return self._append_to_google_doc(timestamp, question, answer)
            else:
                return self._append_to_text_file(timestamp, question, answer)

        except Exception as e:
            print(f"Error appending to Drive file: {e}")
            return False

    def _append_to_google_doc(self, timestamp: str, question: str, answer: str):
        """Append to a Google Doc using Docs API"""
        service = build('docs', 'v1', credentials=self.creds)
        
        # Get current document to find the end index
        doc = service.documents().get(documentId=self.file_id).execute()
        content = doc.get('body').get('content')
        # The last element's endIndex is where we insert
        end_index = content[-1].get('endIndex', 1) - 1

        text_to_insert = f"\nTimestamp: {timestamp}\nQuestion: {question}\nAnswer: {answer}\n----------------------------------------\n"

        requests = [{
            'insertText': {
                'location': {'index': end_index},
                'text': text_to_insert
            }
        }]

        service.documents().batchUpdate(
            documentId=self.file_id,
            body={'requests': requests}
        ).execute()

        print(f"Appended chat log to Google Doc {self.file_id}")
        return True

    def _append_to_text_file(self, timestamp: str, question: str, answer: str):
        """Append to a plain text file using Drive API"""
        service = build('drive', 'v3', credentials=self.creds)

        # 1. Download current content
        request = service.files().get_media(fileId=self.file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        current_content = fh.getvalue().decode('utf-8')

        # 2. Append new content
        new_entry = f"\nTimestamp: {timestamp}\nQuestion: {question}\nAnswer: {answer}\n----------------------------------------\n"
        updated_content = current_content + new_entry

        # 3. Upload updated content
        media = MediaIoBaseUpload(io.BytesIO(updated_content.encode('utf-8')), mimetype='text/plain', resumable=True)
        service.files().update(fileId=self.file_id, media_body=media).execute()

        print(f"Appended chat log to text file {self.file_id}")
        return True
