from fastapi import FastAPI, Depends
from security import check_credentials
from aes_encryption_backend import AES
from pydantic import BaseModel

class crypto_request(BaseModel):
    key: str
    text: str


app = FastAPI()


@app.post("/encode")
async def encode(request: crypto_request, username: str=Depends(check_credentials)) -> str:
    return AES.encode(request.key, request.text)


@app.post("/decode")
async def decode(request: crypto_request, username: str=Depends(check_credentials)) -> str:

    return AES.decode(request.key, request.text)




