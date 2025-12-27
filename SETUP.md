# SETUP INSTRUCTIONS

## For New Developers

1. **Clone the repository**
2. **Copy credentials template:**
   ```bash
   cp credentials.template.json credentials.json
   ```
3. **Get credentials from team lead:**
   - Request the actual Service Account JSON file
   - Or get credentials from secure storage (e.g., 1Password, LastPass)

4. **Update the filename** to match the actual credentials JSON filename format:
   ```
   storage-[PROJECT_ID]-[KEY_ID].json
   ```

5. **Update google_storage.py:**
   - Line 10: Update `SERVICE_ACCOUNT_FILE` to your credentials filename
   - Line 12: Update `FOLDER_ID` to the target Google Drive folder ID

6. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

7. **Test it works:**
   ```bash
   uvicorn app:app --reload
   ```

## Getting Credentials

**Contact:** [Your Team Lead's Name/Email]

**What to request:**
- Service Account JSON file for the chat-storage project
- Google Drive Folder ID where logs are stored

## Never Commit:
- `storage-*.json` files
- Any `credentials.json` file
- `google_drive_file_id.txt`

These are automatically ignored by `.gitignore`.
