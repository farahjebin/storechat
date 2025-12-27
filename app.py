from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from google_storage import GoogleDriveStorage

app = FastAPI(
    title="Chat Storage API",
    description="API to store chat interactions from Custom GPT to a text file on Google Drive.",
    version="1.0.0"
)

# Initialize Google Drive Storage
try:
    storage_client = GoogleDriveStorage()
except Exception as e:
    print(f"Failed to initialize Google Drive Storage: {e}")
    storage_client = None

class ChatLog(BaseModel):
    question: str
    answer: str

@app.post("/store-chat", summary="Store Chat Interaction", operation_id="storeChat")
async def store_chat(chat_log: ChatLog):
    """
    Receives a chat interaction (question and answer) and appends it to a Google Doc.
    """
    if not storage_client:
        raise HTTPException(status_code=500, detail="Storage client is not initialized.")

    success = storage_client.append_chat_log(chat_log.question, chat_log.answer)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save chat log to Google Drive.")
    
    return {"status": "success", "message": "Chat logged successfully."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
