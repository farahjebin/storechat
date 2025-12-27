# Chat Storage API

A lightweight FastAPI backend that automatically stores Custom GPT chat interactions to Google Drive.

## 🚀 Features

- ✅ Automatic chat logging to Google Drive
- ✅ Supports both Google Docs and plain text files
- ✅ Service Account authentication
- ✅ Simple REST API with single POST endpoint
- ✅ Real-time cloud synchronization

## 📋 Prerequisites

- Python 3.8+
- Google Cloud Project with Drive & Docs APIs enabled
- Service Account with JSON credentials

## 🔧 Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd chatstorageapi
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Credentials

1. Copy the template:
   ```bash
   cp credentials.template.json credentials.json
   ```

2. Fill in your Service Account details:
   - Replace `YOUR_PROJECT_ID` with your Google Cloud project ID
   - Replace `YOUR_SERVICE_ACCOUNT_EMAIL` with your service account email
   - Add your actual `private_key` from the downloaded JSON
   - Update other placeholder values

3. **IMPORTANT**: Rename the file to match what your code expects:
   ```bash
   mv credentials.json storage-YOUR_PROJECT_ID-XXXXX.json
   ```

### 5. Update Configuration

Edit `google_storage.py` and update:

```python
SERVICE_ACCOUNT_FILE = 'storage-YOUR_ACTUAL_FILENAME.json'
FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'
```

### 6. Set Up Google Drive

1. Create a folder in Google Drive
2. Share it with your service account email (found in credentials JSON)
3. Copy the folder ID from the URL
4. Create a Google Doc named `chat_history` inside the folder

## 🏃 Running the Application

### Development Mode

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Production Mode

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📡 API Usage

### Endpoint: POST `/store-chat`

**Request Body:**
```json
{
  "question": "What is FastAPI?",
  "answer": "FastAPI is a modern web framework for Python."
}
```

**Success Response:**
```json
{
  "status": "success",
  "message": "Chat logged successfully."
}
```

### Example using curl:

```bash
curl -X POST "http://127.0.0.1:8000/store-chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "Test", "answer": "Works!"}'
```

## 🔐 Security Notes

- **NEVER commit** credentials files (`*.json`) to version control
- The `.gitignore` is configured to exclude sensitive files
- Keep your Service Account JSON file secure
- Use environment variables for production deployments

## 📂 Project Structure

```
chatstorageapi/
├── app.py                          # FastAPI application
├── google_storage.py               # Google Drive/Docs integration
├── requirements.txt                # Python dependencies
├── credentials.template.json       # Template for credentials
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🚢 Deployment

For production deployment, consider:

- **Render/Railway/Fly.io**: Free tier available
- **Google Cloud Run**: Serverless option
- **Heroku**: Easy deployment with add-ons

### Environment Variables for Production:

Instead of JSON files, use environment variables:

```bash
GOOGLE_CREDENTIALS=<base64-encoded-json>
FOLDER_ID=<your-folder-id>
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'google.oauth2'"
```bash
pip install -r requirements.txt
```

### "FileNotFoundError: Service account file not found"
- Ensure credentials file exists in project root
- Check filename matches `SERVICE_ACCOUNT_FILE` in `google_storage.py`

### "StorageQuotaExceeded"
- Make sure the file is owned by YOU (not the service account)
- Service account should only have edit permissions

### API returns 500 error
- Check server logs for detailed error
- Verify Drive folder is shared with service account email
- Ensure both Drive and Docs APIs are enabled

## 📖 Documentation

For detailed setup instructions for clients, see [CLIENT_SETUP_GUIDE.md](./CLIENT_SETUP_GUIDE.md)

## 🤝 Contributing

This is an internal project. For questions or issues, contact the development team.

## 📄 License

Internal use only.

---

**Created by:** [Your Name]  
**Last Updated:** December 2025
