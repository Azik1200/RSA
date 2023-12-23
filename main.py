from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sympy
import random

app = FastAPI()

class KeyPair(BaseModel):
    e: int
    n: int

class Message(BaseModel):
    text: str

def generate_keypair():
    p = sympy.randprime(50, 100)
    q = sympy.randprime(50, 100)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(2, phi_n - 1)
    while sympy.gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)
    d = sympy.mod_inverse(e, phi_n)
    return KeyPair(e=e, n=n), KeyPair(e=d, n=n)

def encrypt(message, public_key):
    cipher_text = [pow(ord(char), public_key.e, public_key.n) for char in message]
    return cipher_text

def decrypt(cipher_text, private_key):
    decrypted_text = ''.join([chr(pow(char, private_key.e, private_key.n)) for char in cipher_text])
    return decrypted_text

@app.post("/generate_keypair", response_model=KeyPair)
def generate_keypair_route():
    public_key, private_key = generate_keypair()
    return public_key

@app.post("/encrypt", response_model=list)
def encrypt_route(message: Message, public_key: KeyPair):
    encrypted_message = encrypt(message.text, public_key)
    return encrypted_message

@app.post("/decrypt", response_model=str)
def decrypt_route(cipher_text: list, private_key: KeyPair):
    decrypted_message = decrypt(cipher_text, private_key)
    return decrypted_message

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
