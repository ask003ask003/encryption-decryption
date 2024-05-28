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


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR,"uploads")


def encrypt_data_aes(data: bytes, key: bytes, iv: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

def decrypt_data_aes(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data

aes_router = APIRouter()


@aes_router.post("/encrypt/aes")
async def encrypt(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1]
    if extension != ".txt":
        return "upload file of type .txt"

    contents = file.file.read()

    new_filename = "{}_{}.txt".format(os.path.splitext(file.filename)[0],timestr)

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR,new_filename)


    aes_key_hex = "8c5d3a69a184869b5b3712cf25de09ec1b273e1d81e99934e9d2d5e8b25c2e33"
    aes_iv_hex = "d39b097d6ef5e22b9e42da41a16f7d19"

    aes_key_bytes = bytes.fromhex(aes_key_hex)
    aes_iv_bytes = bytes.fromhex(aes_iv_hex)

    encrypted_contents = encrypt_data_aes(contents, aes_key_bytes, aes_iv_bytes)


    print(SAVE_FILE_PATH)
    with open(SAVE_FILE_PATH, "wb") as encrypted_file:
        encrypted_file.write(encrypted_contents)

    if os.path.exists(SAVE_FILE_PATH):
            return FileResponse(path=SAVE_FILE_PATH,media_type="application/octet-stream",filename=new_filename) 
    else:
        raise HTTPException(status_code=404, detail="Encrypted file does not exist")

# ,current_user: schemas.UserInDB = Depends(auth.get_current_user),db: Session = Depends(get_db)


@aes_router.post("/decrypt/aes")
async def decrypt(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1]
    if extension != ".txt":
        return "upload file of type .txt"

    new_filename = "{}_{}.txt".format(os.path.splitext(file.filename)[0],timestr)

    SAVE_FILE_PATH = os.path.join(UPLOAD_DIR,new_filename)

    aes_key_hex = "8c5d3a69a184869b5b3712cf25de09ec1b273e1d81e99934e9d2d5e8b25c2e33"
    aes_iv_hex = "d39b097d6ef5e22b9e42da41a16f7d19"
    aes_key_bytes = bytes.fromhex(aes_key_hex)
    aes_iv_bytes = bytes.fromhex(aes_iv_hex)

    encrypted_data = await file.read()

    decrypted_content = decrypt_data_aes(encrypted_data, aes_key_bytes, aes_iv_bytes)

    with open(SAVE_FILE_PATH, "wb") as decrypted_file:
        decrypted_file.write(decrypted_content)

    if os.path.exists(SAVE_FILE_PATH):
        return FileResponse(path=SAVE_FILE_PATH,media_type="application/octet-stream",filename=new_filename) 
    else:
        raise HTTPException(status_code=404, detail="Decrypted file does not exist")