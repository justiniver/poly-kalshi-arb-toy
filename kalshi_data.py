import os
from dotenv import load_dotenv
import requests
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def load_private_key_from_file(file_path):
    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def sign_request(private_key, timestamp, method, path):
    # Strip query parameters from path before signing
    path_without_query = path.split('?')[0]

    # Create the message to sign
    message = f"{timestamp}{method}{path_without_query}".encode('utf-8')

    # Sign with RSA-PSS
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.DIGEST_LENGTH
        ),
        hashes.SHA256()
    )

    # Return base64 encoded
    return base64.b64encode(signature).decode('utf-8')

load_dotenv()
KALSHI_ACCESS_KEY = os.getenv('KALSHI_ACCESS_KEY')
FILE_PATH = "justinkalshi.txt"
KALSHI_PRIVATE_KEY = load_private_key_from_file(FILE_PATH)
timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
method = "GET"
path = "/trade-api/v2/portfolio/balance"

signature = sign_request(KALSHI_PRIVATE_KEY, timestamp, method, path)

headers = {
    "KALSHI-ACCESS-KEY": KALSHI_ACCESS_KEY,
    "KALSHI-ACCESS-SIGNATURE": signature,
    "KALSHI-ACCESS-TIMESTAMP": timestamp
}

base = "https://api.elections.kalshi.com"
response = requests.get(base + path, headers=headers)

print(response.json())
