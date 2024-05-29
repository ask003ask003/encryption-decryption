from fastapi import FastAPI, APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from hashlib import sha256
import os
import time

sha_router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

timestr = time.strftime("%Y%m%d-%H%M%S")

# Define the ideal hash string for verification purposes
IDEAL_HASH = "df7ab51bdf36c772240a52a76b7123cfd0af29516cd6d581324763b3295d1091"

@sha_router.post("/encrypt/sha256")
async def hash_file(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1]
    if extension != ".txt":
        return {"error": "Upload file of type .txt"}

    
    data = await file.read()
    hash_object = sha256(data)
    hashed_data = hash_object.hexdigest()
    global IDEAL_HASH 
    IDEAL_HASH = hashed_data
    
    return "Hashed succesfully"

@sha_router.post("/decrypt/sha256")
async def verify_file(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1]
    if extension != ".txt":
        return {"error": "Upload file of type .txt"}

    data = await file.read()
    hash_object = sha256(data)
    computed_hash = hash_object.hexdigest()


    
    if computed_hash == IDEAL_HASH:
        return "match"
    else:
        return "mismatch"

app = FastAPI()

app.include_router(sha_router, prefix="/sha256")
