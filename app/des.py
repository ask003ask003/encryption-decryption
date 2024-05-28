from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import os
from app import auth, models, schemas, security
from app.db import get_db
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from starlette.responses import FileResponse
import time
from Crypto.Cipher import DES,PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import os
import tempfile
import base64
timestr = time.strftime("%Y%m%d-%H%M%S")


des_router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR,"uploads")

DES_KEY = b's3cr3tK3' 
BLOCK_SIZE = 8

def pad(data):
    padding_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
    padding = bytes([padding_len] * padding_len)
    return data + padding

def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]

@des_router.post("/encrypt/des")
async def encrypt_file(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1]
    if extension != ".txt":
        return "upload file of type .txt"
    new_filename = "{}_{}.txt".format(os.path.splitext(file.filename)[0],timestr)

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR,new_filename)
    
    cipher = DES.new(DES_KEY, DES.MODE_ECB)
    data = await file.read()
    padded_data = pad(data)
    encrypted_data = cipher.encrypt(padded_data)
    
    with open(SAVE_FILE_PATH, 'wb') as f:
        f.write(encrypted_data)
    
    return FileResponse(path=SAVE_FILE_PATH,media_type="application/octet-stream",filename=new_filename)

@des_router.post("/decrypt/des")
async def decrypt_file(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1]
    if extension != ".txt":
        return "upload file of type .txt"
    new_filename = "{}_{}.txt".format(os.path.splitext(file.filename)[0],timestr)

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR,new_filename)
    
    cipher = DES.new(DES_KEY, DES.MODE_ECB)
    data = await file.read()
    decrypted_data = cipher.decrypt(data)
    unpadded_data = unpad(decrypted_data)
    
    with open(SAVE_FILE_PATH, 'wb') as f:
        f.write(unpadded_data)
    
    return FileResponse(path=SAVE_FILE_PATH,media_type="application/octet-stream",filename=new_filename)