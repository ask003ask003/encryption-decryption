
from fastapi import FastAPI
import uvicorn
from app import models
from app.db import engine
from app.aes import aes_router
from app.routes import router
from app.des import des_router
from app.rsa import rsa_router
from app.dummy import dummy_router
from app.sha import sha_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(router)
app.include_router(aes_router)
app.include_router(des_router)
app.include_router(rsa_router)
app.include_router(sha_router)
app.include_router(dummy_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=5555)