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

rsa_router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR,"uploads")

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

PRIVATE_KEY, PUBLIC_KEY = generate_keys()

def encrypt_data(data, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

def decrypt_data(data, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    decrypted_data = cipher.decrypt(data)
    return decrypted_data







@rsa_router.post("/encrypt/rsa")
async def encrypt_file(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1]
    if extension != ".txt":
        return "upload file of type .txt"
    new_filename = "{}_{}.txt".format(os.path.splitext(file.filename)[0],timestr)

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR,new_filename)
    contents = await file.read()
    start_time = time.time()
    encrypted_data = encrypt_data(contents, PUBLIC_KEY)
    total_time = time.time() - start_time
    
    with open(SAVE_FILE_PATH,"wb") as temp_file:
        temp_file.write(encrypted_data)
    
    return FileResponse(path=SAVE_FILE_PATH,media_type="application/octet-stream",filename=new_filename,headers={"x- Total-Time": str(total_time)})



@rsa_router.post("/decrypt/rsa")
async def decrypt_file(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1]
    if extension != ".txt":
        return "upload file of type .txt"
    new_filename = "{}_{}.txt".format(os.path.splitext(file.filename)[0],timestr)

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR,new_filename)

    contents = await file.read()
    decrypted_data = decrypt_data(contents, PRIVATE_KEY)
    
    with open(SAVE_FILE_PATH,"wb") as temp_file:
        temp_file.write(decrypted_data)
    
    return FileResponse(path=SAVE_FILE_PATH,media_type="application/octet-stream",filename=new_filename)